"""Binary sensor platform for berluf_selen_500."""

from __future__ import annotations
import importlib
from typing import TYPE_CHECKING
from venv import logger

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .data import Berluf_selen_500_ConfigEntry
from .defs import LOGGER
from .entity import Berluf_selen_500_AsyncEntry

from .berluf_selen_500.funcs import Bypass, Heater, Pump

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Berluf_selen_500_ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        [
            Berluf_selen_500_bypass(
                entry=entry,
                entity_description=BinarySensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 bypass indicator",
                    # device_class=BinarySensorDeviceClass.CONNECTIVITY, # FIXME For now Set to "None"
                ),
            ),
            Berluf_selen_500_heater(
                entry=entry,
                entity_description=BinarySensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 heater indicator",
                    # device_class=BinarySensorDeviceClass.CONNECTIVITY, # FIXME For now Set to "None"
                ),
            ),
            Berluf_selen_500_pump(
                entry=entry,
                entity_description=BinarySensorEntityDescription(
                    key="berluf_selen_500",
                    name="Berluf Selen 500 pump indicator",
                    # device_class=BinarySensorDeviceClass.CONNECTIVITY, # FIXME For now Set to "None"
                ),
            ),
        ]
    )


class Berluf_selen_500_bypass(Berluf_selen_500_AsyncEntry, BinarySensorEntity):
    """berluf_selen_500 bypass indicator."""

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(entry)
        self.entity_description = entity_description

        self._impl = Bypass(entry.runtime_data.get_device(), self._callb)
        return

    def _callb(self, val: bool):
        LOGGER.debug(f"Bypass: {self._impl.get()}")
        self._fire_change_callb()

    @property
    def is_on(self) -> bool:
        """Return state of the recuperators bypass (True = ON)."""  # TODO Add Enum for on and off?
        LOGGER.debug(f"Bypass reading: {self._impl.get()}")
        return self._impl.get()

    async def async_update(self) -> None:
        """Wait till state is changed."""
        await self._wait_change_callb()


class Berluf_selen_500_heater(Berluf_selen_500_AsyncEntry, BinarySensorEntity):
    """berluf_selen_500 heater indicator."""

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(entry, "heater")
        self.entity_description = entity_description

        self._impl = Heater(entry.runtime_data.get_device(), self._callb)
        return

    def _callb(self, val: bool):
        self._fire_change_callb()

    @property
    def is_on(self) -> bool:
        """Return state of the recuperators bypass (True = ON)."""  # TODO Add Enum for on and off?
        return self._impl.get()

    async def async_update(self) -> None:
        """Wait till state is changed."""
        await self._wait_change_callb()


class Berluf_selen_500_pump(Berluf_selen_500_AsyncEntry, BinarySensorEntity):
    """berluf_selen_500 pump indicator."""

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(entry, "pump")
        self.entity_description = entity_description

        self._impl = Pump(entry.runtime_data.get_device(), self._callb)
        return

    def _callb(self, val: bool):
        self._fire_change_callb()

    @property
    def is_on(self) -> bool:
        """Return state of the recuperators bypass (True = ON)."""  # TODO Add Enum for on and off?
        return self._impl.get()

    async def async_update(self) -> None:
        """Wait till state is changed."""
        await self._wait_change_callb()
