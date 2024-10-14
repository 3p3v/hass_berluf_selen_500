"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import decimal

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .data import Berluf_selen_500_ConfigEntry
from .defs import LOGGER
from .entity import Berluf_selen_500_Entry

from .berluf_selen_500.funcs import GWC

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Berluf_selen_500_ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        [
            Berluf_selen_500_GWC(
                entry=entry,
                entity_description=SwitchEntityDescription(
                    key="berluf_selen_500",
                    name="Selen GWC switch",
                ),
            ),
        ]
    )


class Berluf_selen_500_GWC(Berluf_selen_500_Entry, SwitchEntity):
    """berluf_selen_500 heater cooler switch."""

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry, "GWC")
        self.entity_description = entity_description

        self._impl = GWC(entry.runtime_data.get_device())

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._impl.get()

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self._impl.set(True)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self._impl.set(False)
