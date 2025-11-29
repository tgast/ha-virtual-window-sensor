"""Config flow for Virtual Window Sensor integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_TEMPERATURE_SENSOR,
    CONF_TEMP_DROP,
    CONF_TIME_WINDOW,
    CONF_NAME,
    DEFAULT_TEMP_DROP,
    DEFAULT_TIME_WINDOW,
)

_LOGGER = logging.getLogger(__name__)


class VirtualWindowSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Window Sensor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate that the temperature sensor exists
            temp_sensor = user_input[CONF_TEMPERATURE_SENSOR]
            if not self.hass.states.get(temp_sensor):
                errors[CONF_TEMPERATURE_SENSOR] = "sensor_not_found"
            else:
                # Create unique ID based on temperature sensor
                await self.async_set_unique_id(temp_sensor)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TEMPERATURE_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="temperature",
                    ),
                ),
                vol.Optional(
                    CONF_TEMP_DROP, default=DEFAULT_TEMP_DROP
                ): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=5.0)),
                vol.Optional(
                    CONF_TIME_WINDOW, default=DEFAULT_TIME_WINDOW
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VirtualWindowSensorOptionsFlow(config_entry)


class VirtualWindowSensorOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Virtual Window Sensor."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_TEMP_DROP,
                        default=self.config_entry.options.get(
                            CONF_TEMP_DROP,
                            self.config_entry.data.get(CONF_TEMP_DROP, DEFAULT_TEMP_DROP),
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=5.0)),
                    vol.Optional(
                        CONF_TIME_WINDOW,
                        default=self.config_entry.options.get(
                            CONF_TIME_WINDOW,
                            self.config_entry.data.get(CONF_TIME_WINDOW, DEFAULT_TIME_WINDOW),
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                }
            ),
        )
