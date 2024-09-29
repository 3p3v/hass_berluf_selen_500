"""BlueprintEntity class."""

from __future__ import annotations
import asyncio

from homeassistant.helpers.device_registry import DeviceInfo
# from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .defs import ATTRIBUTION
from .data import Berluf_selen_500_ConfigEntry


class Berluf_selen_500_Entry:
    """ berluf_selen_500 entry """

    _attr_attribution = ATTRIBUTION

    def __init__(self, entry: Berluf_selen_500_ConfigEntry) -> None:
        """Initialize."""
        super().__init__()
        self._attr_unique_id = entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    entry.domain,
                    entry.entry_id,
                ),
            },
        )
        return
        
class Berluf_selen_500_AsyncEntry(Berluf_selen_500_Entry):
    """ berluf_selen_500 entry for async updating """
    
    def __init__(self, entry: Berluf_selen_500_ConfigEntry) -> None:
        super().__init__(entry)
        
        self._event = asyncio.Event()
        return
    
    def _fire_change_callb(self):
        """ Inform about data change """
        self._event.set()
        
    async def _wait_change_callb(self):
        """ Wait for data change """
        await self._event.wait()