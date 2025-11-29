"""Binary sensor platform for Virtual Window Sensor."""
import logging
from datetime import timedelta
from collections import deque

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_TEMPERATURE_SENSOR,
    CONF_TEMP_DROP,
    CONF_TIME_WINDOW,
    CONF_NAME,
    DEFAULT_TEMP_DROP,
    DEFAULT_TIME_WINDOW,
    ATTR_TEMPERATURE,
    ATTR_PREVIOUS_TEMPERATURE,
    ATTR_TEMPERATURE_DROP,
    ATTR_TIME_WINDOW,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Virtual Window Sensor binary sensor."""
    sensor = VirtualWindowSensor(hass, config_entry)
    async_add_entities([sensor], True)


class VirtualWindowSensor(BinarySensorEntity):
    """Representation of a Virtual Window Sensor."""

    _attr_device_class = BinarySensorDeviceClass.WINDOW
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._config_entry = config_entry
        self._attr_name = config_entry.data[CONF_NAME]
        self._attr_unique_id = f"{DOMAIN}_{config_entry.entry_id}"
        
        self._temperature_sensor = config_entry.data[CONF_TEMPERATURE_SENSOR]
        self._temp_drop_threshold = config_entry.options.get(
            CONF_TEMP_DROP,
            config_entry.data.get(CONF_TEMP_DROP, DEFAULT_TEMP_DROP)
        )
        self._time_window = config_entry.options.get(
            CONF_TIME_WINDOW,
            config_entry.data.get(CONF_TIME_WINDOW, DEFAULT_TIME_WINDOW)
        )
        
        # Store temperature history with timestamps
        self._temperature_history = deque(maxlen=100)
        self._current_temperature = None
        self._is_open = False
        self._unsub_state_changed = None

    @property
    def is_on(self) -> bool:
        """Return true if the window is open."""
        return self._is_open

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            ATTR_TIME_WINDOW: self._time_window,
            ATTR_TEMPERATURE_DROP: self._temp_drop_threshold,
        }
        
        if self._current_temperature is not None:
            attrs[ATTR_TEMPERATURE] = self._current_temperature
            
        if self._temperature_history:
            oldest_in_window = self._get_temperature_at_time_ago(self._time_window)
            if oldest_in_window is not None:
                attrs[ATTR_PREVIOUS_TEMPERATURE] = oldest_in_window
                attrs["calculated_drop"] = round(oldest_in_window - self._current_temperature, 2)
                
        return attrs

    async def async_added_to_hass(self) -> None:
        """Register callbacks when entity is added."""
        # Get initial state
        state = self.hass.states.get(self._temperature_sensor)
        if state and state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            try:
                temp = float(state.state)
                self._current_temperature = temp
                self._add_temperature_reading(temp)
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Could not convert initial temperature state to float: %s",
                    state.state
                )

        # Subscribe to state changes
        self._unsub_state_changed = async_track_state_change_event(
            self.hass,
            [self._temperature_sensor],
            self._async_temperature_changed,
        )

        # Listen to options updates
        self._config_entry.async_on_unload(
            self._config_entry.add_update_listener(self._async_options_updated)
        )

    async def async_will_remove_from_hass(self) -> None:
        """Cleanup when entity is removed."""
        if self._unsub_state_changed:
            self._unsub_state_changed()

    @callback
    def _async_temperature_changed(self, event) -> None:
        """Handle temperature sensor state changes."""
        new_state = event.data.get("new_state")
        
        if new_state is None or new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return

        try:
            new_temp = float(new_state.state)
        except (ValueError, TypeError):
            _LOGGER.warning(
                "Could not convert temperature state to float: %s",
                new_state.state
            )
            return

        self._current_temperature = new_temp
        self._add_temperature_reading(new_temp)
        self._update_window_state()
        self.async_write_ha_state()

    def _add_temperature_reading(self, temperature: float) -> None:
        """Add a temperature reading to history."""
        now = dt_util.utcnow()
        self._temperature_history.append((now, temperature))
        
        # Clean old entries (older than time_window + buffer)
        cutoff = now - timedelta(seconds=self._time_window + 60)
        while self._temperature_history and self._temperature_history[0][0] < cutoff:
            self._temperature_history.popleft()

    def _get_temperature_at_time_ago(self, seconds: int) -> float | None:
        """Get temperature from N seconds ago."""
        if not self._temperature_history:
            return None
            
        target_time = dt_util.utcnow() - timedelta(seconds=seconds)
        
        # Find the closest temperature reading to target_time
        closest_reading = None
        min_diff = float('inf')
        
        for timestamp, temp in self._temperature_history:
            diff = abs((timestamp - target_time).total_seconds())
            if diff < min_diff:
                min_diff = diff
                closest_reading = temp
                
        # Only return if we have a reading within reasonable range (±10 seconds)
        if min_diff <= 10:
            return closest_reading
            
        return None

    def _update_window_state(self) -> None:
        """Update the window open/closed state based on temperature drop."""
        if self._current_temperature is None:
            self._is_open = False
            return
            
        old_temp = self._get_temperature_at_time_ago(self._time_window)
        
        if old_temp is None:
            # Not enough history yet
            self._is_open = False
            return
            
        temp_drop = old_temp - self._current_temperature
        
        _LOGGER.debug(
            "Temperature drop check: old=%.2f, current=%.2f, drop=%.2f, threshold=%.2f",
            old_temp,
            self._current_temperature,
            temp_drop,
            self._temp_drop_threshold
        )
        
        # Window is "open" if temperature dropped by more than threshold
        self._is_open = temp_drop > self._temp_drop_threshold

    @staticmethod
    async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Handle options update."""
        await hass.config_entries.async_reload(entry.entry_id)
