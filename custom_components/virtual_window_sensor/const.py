"""Constants for the Virtual Window Sensor integration."""

DOMAIN = "virtual_window_sensor"

# Configuration
CONF_TEMPERATURE_SENSOR = "temperature_sensor"
CONF_TEMP_DROP = "temp_drop"
CONF_TIME_WINDOW = "time_window"
CONF_NAME = "name"

# Defaults
DEFAULT_TEMP_DROP = 0.3  # Degrees Celsius
DEFAULT_TIME_WINDOW = 30  # Seconds

# Attributes
ATTR_TEMPERATURE = "temperature"
ATTR_PREVIOUS_TEMPERATURE = "previous_temperature"
ATTR_TEMPERATURE_DROP = "temperature_drop"
ATTR_TIME_WINDOW = "time_window"
