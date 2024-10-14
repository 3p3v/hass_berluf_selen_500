"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import decimal

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.const import UnitOfTemperature

from .berluf_selen_500.modbus_impl.asyncio.timer import Asyncio_timer_factory

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
    timer = Berluf_selen_500_error(
        entry=entry,
        entity_description=SensorEntityDescription(
            key="berluf_selen_500",
            name="Selen error indicator",
        ),
    )
    entry.runtime_data.set_timer(timer)

    async_add_entities(
        [
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_01,
                thermometer_name="01",
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Selen temp. 01",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_02,
                thermometer_name="02",
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Selen temp. 02",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_03,
                thermometer_name="03",
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Selen temp. 03",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_04,
                thermometer_name="04",
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Selen temp. 04",
                    # icon="mdi:format-quote-close",
                ),
            ),
            Berluf_selen_500_thermometer(
                thermometer_class=Thermometer_05,
                thermometer_name="05",
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_500",
                    name="Selen temp. 05",
                    # icon="mdi:format-quote-close",
                ),
            ),
            timer,
        ]
    )


class Berluf_selen_500_thermometer(Berluf_selen_500_AsyncEntry, SensorEntity):
    """berluf_selen_500 thermometer."""

    def __init__(
        self,
        thermometer_class,
        thermometer_name,  # TODO delete, do not set name at all
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry, thermometer_name)
        self.entity_description = entity_description

        # self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

        self._impl = thermometer_class(entry.runtime_data.get_device(), self._callb)

    def _callb(self, val: int) -> None:
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

        self._impl = Error(
            entry.runtime_data.get_device(), Asyncio_timer_factory(), self._callb
        )
        self._ec = None

    def _callb(self, ecs: list[Error.Error]) -> None:
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

    def cancel(self) -> None:
        """Cancel timer (call when object needs to be deleted)."""
        self._impl.cancel()

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self._ec

    async def async_update(self) -> None:
        """Wait till state is changed."""
        await self._wait_change_callb()
