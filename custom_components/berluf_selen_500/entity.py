"""BlueprintEntity class."""

from __future__ import annotations
import asyncio

from homeassistant.helpers.device_registry import DeviceInfo
# from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .data import Berluf_selen_500_ConfigEntry


class Berluf_selen_500_Entry:
    """berluf_selen_500 entry."""

    # _attr_attribution = ATTRIBUTION
    _class_id = 0

    def __init__(
        self, entry: Berluf_selen_500_ConfigEntry, unique: str | None = None
    ) -> None:
        """Initialize."""
        type(self)._class_id += 1
        if unique is None:
            self._attr_unique_id = entry.entry_id + str(type(self)._class_id)
        else:
            self._attr_unique_id = entry.entry_id + unique

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
    """berluf_selen_500 entry for async updating."""

    def __init__(
        self, entry: Berluf_selen_500_ConfigEntry, unique: str | None = None
    ) -> None:
        super().__init__(entry, unique)

        self._event = asyncio.Event()
        return

    def _fire_change_callb(self) -> None:
        """Inform about data change."""
        self._event.set()

    async def _wait_change_callb(self) -> None:
        """Wait for data change."""
        await self._event.wait()
        self._event.clear()
