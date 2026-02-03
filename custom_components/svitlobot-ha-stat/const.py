"""Constants for Svitlobot integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "svitlobot"
API_URL: Final = "https://api.svitlobot.in.ua/website/getChannels"

# Update interval in seconds (5 minutes)
UPDATE_INTERVAL: Final = 300

# Status codes
STATUS_POWER_ON: Final = 1
STATUS_POWER_OFF: Final = (2, 3)

# City filter
CITY_KYIV: Final = "Київ"

# Sensor keys
SENSOR_TOTAL_CHANNELS: Final = "total_channels"
SENSOR_POWER_ON: Final = "power_on"
SENSOR_POWER_OFF: Final = "power_off"
SENSOR_POWER_ON_PERCENT: Final = "power_on_percent"
SENSOR_POWER_OFF_PERCENT: Final = "power_off_percent"
