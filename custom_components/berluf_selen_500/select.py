"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import decimal

from homeassistant.components.select import SelectEntity, SelectEntityDescription

from .data import Berluf_selen_500_ConfigEntry
from .defs import LOGGER
from .entity import Berluf_selen_500_Entry

from .berluf_selen_500.funcs import Heater_cooler

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Berluf_selen_500_ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    async_add_entities(
        [
            Berluf_selen_500_heater_cooler(
                entry=entry,
                entity_description=SelectEntityDescription(
                    key="berluf_selen_500",
                    name="Selen heater cooler switch",
                    options=Heater_cooler.Mode._member_names_,
                    # icon="mdi:format-quote-close",
                ),
            ),
        ]
    )


class Berluf_selen_500_heater_cooler(Berluf_selen_500_Entry, SelectEntity):
    """berluf_selen_500 heater cooler switch."""

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: SelectEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry)
        self.entity_description = entity_description

        self._impl = Heater_cooler(entry.runtime_data.get_device())

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        return self._impl.get().name

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._impl.set(Heater_cooler.Mode[option])
