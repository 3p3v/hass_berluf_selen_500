from typing import Callable, override
import asyncio

from homeassistant.helpers.storage import Store
from homeassistant.core import HomeAssistant

from .defs import LOGGER

from .berluf_selen_500.modbus_slave.persistant import (
    Collective_persistant,
)
from .berluf_selen_500.modbus_slave.memory import Memory


class Hass_persistant_loader:
    def __init__(
        self, subkey: str, store: Store[dict[str, dict[int, list[int]]]]
    ) -> None:
        self._subkey = subkey
        self._store = store

    async def load(self) -> dict[int, list[int]]:
        data = await self._store.async_load()
        if data is not None:
            data_int = dict[int, list[int]]()
            for a, v in data[self._subkey].items():
                data_int[int(a)] = v

            return data_int
        else:
            raise RuntimeError("Error while retreiving saved data.")


class Hass_rapid_persistant(Collective_persistant):
    def __init__(
        self, subkey: str, memory: Memory, store: Store[dict[str, dict[int, list[int]]]]
    ) -> None:
        self._subkey = subkey
        self._memory = memory
        self._store = store
        self._action_done = False

    async def _perform_action(self) -> None:
        try:
            if not self._action_done:
                await self._store.async_save(
                    {self._subkey: self._memory.get_all_multi_vals()}
                )
                self._action_done = True
        except Exception as ec:
            LOGGER.critical(f"Action needed. Cannot save user settings: {ec}")

    @override
    def save(self) -> None:
        self._action_done = False
        asyncio.ensure_future(self._perform_action())
        return
