""" Binary sensor platform for berluf_selen_500 """

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import Berluf_selen_500_ConfigEntry
    
    # Underlying bypass detection
    from .recup.device import Recup_device
    from .recup.funcs import Bypass
    
    #
    from .entity import Berluf_selen_500_AsyncEntry
    

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="berluf_selen_500",
        name="Berluf Selen 500 Bypass indicator",
        # device_class=BinarySensorDeviceClass.CONNECTIVITY, # FIXME For now Set to "None"
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Berluf_selen_500_ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """ Set up the binary_sensor platform. """
    async_add_entities(
        Berluf_selen_500_bypass(
            entry=entry,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class Berluf_selen_500_bypass(Berluf_selen_500_AsyncEntry, BinarySensorEntity):
    """ berluf_selen_500 bypass indicator """

    def __init__(
        self,
        entry: Berluf_selen_500_ConfigEntry,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super(entry).__init__()
        self.entity_description = entity_description
        
        self._impl: Bypass = Bypass(entry.runtime_data.get_device(), lambda x: self._fire_change_callb())
        return

    @property
    def is_on(self) -> bool:
        """ Return state of the recuperators bypass (True = ON) """ # TODO Add Enum for on and off?
        return self._impl.get()
    
    async def async_update(self) -> None:
        """ Wait till state is changed """
        await self._wait_change_callb()