"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import decimal

from homeassistant.components.number import NumberEntity, NumberEntityDescription

from .data import Berluf_selen_500_ConfigEntry
from .defs import LOGGER
from .entity import Berluf_selen_500_Entry

from .berluf_selen_500.funcs import Temperature_sensor, Supply_fan, Exhaust_fan

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Berluf_selen_500_ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    async_add_entities(
        [
            Berluf_selen_500_temperature_sensor(
                entry=entry,
                entity_description=NumberEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 temperature sensor",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_fan(
                fan_class=Supply_fan,
                entry=entry,
                entity_description=NumberEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 supply fan",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_fan(
                fan_class=Exhaust_fan,
                entry=entry,
                entity_description=NumberEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 exhaust fan",
                    # icon="mdi:format-quote-close",
                ),
            ),
        ]
    )


class Berluf_selen_500_temperature_sensor(Berluf_selen_500_Entry, NumberEntity):
    """berluf_selen_500 temperature sensor."""

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: NumberEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry)

        self._attr_native_max_value: float = 100.0
        self._attr_native_min_value: float = 0.0
        self._attr_native_step: float = 1.0

        self.entity_description = entity_description
        self._impl = Temperature_sensor(entry.runtime_data.get_device())

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._impl.set(int(value))

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        return float(self._impl.get())


class Berluf_selen_500_fan(Berluf_selen_500_Entry, NumberEntity):
    """berluf_selen_500 fan."""

    def __init__(
        self,
        fan_class,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: NumberEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry)
        self._attr_native_max_value: float = 50.0
        self._attr_native_min_value: float = 0.0
        self._attr_native_step: float = 1.0

        self.entity_description = entity_description
        self._impl = fan_class(entry.runtime_data.get_device())

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._impl.set(int(value))

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        return float(self._impl.get())
