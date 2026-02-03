"""Sensor platform for Svitlobot."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SvitlobotCoordinator, SvitlobotData

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class SvitlobotSensorEntityDescription(SensorEntityDescription):
    """Describes Svitlobot sensor entity."""

    value_fn: Callable[[SvitlobotData], int | float | None]


SENSORS: tuple[SvitlobotSensorEntityDescription, ...] = (
    SvitlobotSensorEntityDescription(
        key="total_channels",
        translation_key="total_channels",
        icon="mdi:counter",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.total_channels,
    ),
    SvitlobotSensorEntityDescription(
        key="power_on",
        translation_key="power_on",
        icon="mdi:lightbulb-on",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.power_on,
    ),
    SvitlobotSensorEntityDescription(
        key="power_off",
        translation_key="power_off",
        icon="mdi:lightbulb-off",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.power_off,
    ),
    SvitlobotSensorEntityDescription(
        key="power_on_percent",
        translation_key="power_on_percent",
        icon="mdi:lightbulb-on-outline",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.power_on_percent,
    ),
    SvitlobotSensorEntityDescription(
        key="power_off_percent",
        translation_key="power_off_percent",
        icon="mdi:lightbulb-off-outline",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.power_off_percent,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Svitlobot sensors based on a config entry."""
    coordinator: SvitlobotCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        SvitlobotSensor(coordinator, description, entry)
        for description in SENSORS
    )


class SvitlobotSensor(CoordinatorEntity[SvitlobotCoordinator], SensorEntity):
    """Representation of a Svitlobot sensor."""

    entity_description: SvitlobotSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SvitlobotCoordinator,
        description: SvitlobotSensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": f"Svitlobot {entry.data.get('city', 'Київ')}",
            "manufacturer": "Svitlobot",
            "model": "Power Statistics",
        }

    @property
    def native_value(self) -> int | float | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
