"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import decimal

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import PERCENTAGE

from .data import Berluf_selen_500_ConfigEntry
from .defs import LOGGER
from .entity import Berluf_selen_500_Entry

from .berluf_selen_500.funcs import Fans_initializer, Supply_fan, Exhaust_fan

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Berluf_selen_500_ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    fans_initializer = Fans_initializer(entry.runtime_data.get_device())

    exhaust_fan = Berluf_selen_500_exhaust_fan(
        initializer=fans_initializer,
        entry=entry,
        entity_description=NumberEntityDescription(
            key="berluf_selen_500",
            name="Berluf Selen 500 exhaust fan",
            # icon="mdi:format-quote-close",
        ),
    )

    async_add_entities([exhaust_fan])

    async_add_entities(
        [
            Berluf_selen_500_supply_fan(
                initializer=fans_initializer,
                hass=hass,
                exhaust_fan=exhaust_fan,
                entry=entry,
                entity_description=NumberEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 supply fan",
                    # icon="mdi:format-quote-close",
                ),
            ),
        ]
    )


class Berluf_selen_500_supply_fan(Berluf_selen_500_Entry, NumberEntity):
    """berluf_selen_500 fan."""

    def __init__(
        self,
        hass: HomeAssistant,
        exhaust_fan: Berluf_selen_500_exhaust_fan,
        initializer: Fans_initializer,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: NumberEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry, "supply_fan")
        self._attr_native_max_value: float = 100.0
        self._attr_native_min_value: float = 0.0
        self._attr_native_step: float = 1.0
        self._attr_native_unit_of_measurement = PERCENTAGE

        self.entity_description = entity_description
        self._impl = Supply_fan(initializer)

        self._hass = hass
        self._exhaust_fan = exhaust_fan

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._impl.set(int(value))
        # TODO set exhaust fan attrs
        # Update exhaust fan
        self._hass.services.call(
            "homeassistant", "update_entity", {"entity_id": self._exhaust_fan.entity_id}
        )

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        return float(self._impl.get())


class Berluf_selen_500_exhaust_fan(Berluf_selen_500_Entry, NumberEntity):
    """berluf_selen_500 fan."""

    def __init__(
        self,
        initializer: Fans_initializer,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: NumberEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry, "exhaust_fan")
        self._attr_native_step: float = 1.0
        self._attr_native_unit_of_measurement = PERCENTAGE

        self.entity_description = entity_description
        self._impl = Exhaust_fan(initializer)

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._impl.set(int(value))

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        return float(self._impl.get())

    @property
    def native_max_value(self) -> float:  # TODO DELETE
        return self._impl._device.holding_registers.get_single_val(
            self._impl._addr_supply
        )

    @property
    def native_min_value(self) -> float:  # TODO DELETE
        return max(
            self._impl._device.holding_registers.get_single_val(self._impl._addr_supply)
            - 20,
            0,
        )
