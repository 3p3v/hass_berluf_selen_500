"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import decimal

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .data import Berluf_selen_500_ConfigEntry
from .defs import LOGGER
from .entity import Berluf_selen_500_AsyncEntry

from .berluf_selen_500.funcs import (
    Thermometer_01,
    Thermometer_02,
    Thermometer_03,
    Thermometer_04,
    Thermometer_05,
    Error,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Berluf_selen_500_ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        [
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_01,
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 thermometer 01",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_02,
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 thermometer 02",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_03,
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 thermometer 03",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_04,
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 thermometer 04",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_05,
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 thermometer 05",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_error(
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 error indicator",
                    # icon="mdi:format-quote-close",
                ),
            ),
        ]
    )


class Berluf_selen_500_thermometer(Berluf_selen_500_AsyncEntry, SensorEntity):
    """berluf_selen_500 thermometer."""

    def __init__(
        self,
        thermometer_class,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry)
        self.entity_description = entity_description

        self._impl = thermometer_class(entry.runtime_data.get_device(), self._callb)

    def _callb(self, val: int):
        self._fire_change_callb()

    @property
    def native_value(self) -> decimal.Decimal | None:
        """Return the native value of the sensor."""
        temp = self._impl.get()
        if temp == int("11111111"):
            return None
        else:
            return decimal.Decimal(temp)

    async def async_update(self) -> None:
        """Wait till state is changed."""
        await self._wait_change_callb()


class Berluf_selen_500_error(Berluf_selen_500_AsyncEntry, SensorEntity):
    """berluf_selen_500 error indicator."""

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry, "error")
        self.entity_description = entity_description

        self._impl = Error(entry.runtime_data.get_device(), self._callb)
        self._ec = None

    def _callb(self, ecs: list[Error.Error]):
        LOGGER.debug("Error callback.")
        # Save errors
        if len(ecs) == 0:
            self._ec = None
        else:
            self._ec = ecs[0].name
            for e in ecs[1:]:
                self._ec += f", {e.name}"

        # Try fixing recuperator
        self._impl.reset()

        self._fire_change_callb()
        LOGGER.debug("Error callback end.")

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self._ec

    async def async_update(self) -> None:
        """Wait till state is changed."""
        await self._wait_change_callb()
