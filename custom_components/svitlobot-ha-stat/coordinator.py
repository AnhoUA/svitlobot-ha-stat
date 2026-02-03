"""DataUpdateCoordinator for Svitlobot."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import TYPE_CHECKING

from aiohttp import ClientError, ClientSession, ClientTimeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_URL,
    CITY_KYIV,
    DOMAIN,
    STATUS_POWER_ON,
    UPDATE_INTERVAL,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


@dataclass
class SvitlobotData:
    """Class to hold Svitlobot statistics data."""

    total_channels: int
    power_on: int
    power_off: int
    power_on_percent: float
    power_off_percent: float


class SvitlobotCoordinator(DataUpdateCoordinator[SvitlobotData]):
    """Svitlobot data update coordinator."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        city: str = CITY_KYIV,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._session = session
        self._city = city

    async def _async_update_data(self) -> SvitlobotData:
        """Fetch data from API."""
        try:
            timeout = ClientTimeout(total=30)
            async with self._session.get(API_URL, timeout=timeout) as response:
                response.raise_for_status()
                text = await response.text()
        except ClientError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

        return self._parse_data(text)

    def _parse_data(self, raw_data: str) -> SvitlobotData:
        """Parse raw API response and calculate statistics."""
        lines = raw_data.strip().split("\n")

        total = 0
        power_on = 0
        power_off = 0

        for line in lines:
            if not line.strip():
                continue

            parts = line.split(";&;")
            if len(parts) < 5:
                continue

            try:
                status = int(parts[0])
                location = parts[2]
            except (ValueError, IndexError):
                continue

            # Filter by city
            if self._city not in location:
                continue

            total += 1

            if status == STATUS_POWER_ON:
                power_on += 1
            else:
                power_off += 1

        # Calculate percentages
        if total > 0:
            power_on_percent = round((power_on / total) * 100, 1)
            power_off_percent = round((power_off / total) * 100, 1)
        else:
            power_on_percent = 0.0
            power_off_percent = 0.0

        _LOGGER.debug(
            "Svitlobot stats for %s: total=%d, on=%d (%.1f%%), off=%d (%.1f%%)",
            self._city,
            total,
            power_on,
            power_on_percent,
            power_off,
            power_off_percent,
        )

        return SvitlobotData(
            total_channels=total,
            power_on=power_on,
            power_off=power_off,
            power_on_percent=power_on_percent,
            power_off_percent=power_off_percent,
        )
