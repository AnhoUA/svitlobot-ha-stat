"""Binary sensor platform for Svitlobot."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SvitlobotCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Svitlobot binary sensors based on a config entry."""
    coordinator: SvitlobotCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([SvitlobotConnectivitySensor(coordinator, entry)])


class SvitlobotConnectivitySensor(
    CoordinatorEntity[SvitlobotCoordinator], BinarySensorEntity
):
    """Binary sensor for Svitlobot API connectivity."""

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_translation_key = "api_connectivity"

    def __init__(
        self,
        coordinator: SvitlobotCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_api_connectivity"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": f"Svitlobot {entry.data.get('city', 'Київ')}",
            "manufacturer": "Svitlobot",
            "model": "Power Statistics",
        }

    @property
    def is_on(self) -> bool:
        """Return True if API is connected."""
        return self.coordinator.last_update_success
