from ...modbus_slave.timer import Timer, Timer_factory
import asyncio
from typing import Callable


class Asyncio_timer(Timer):
    def __init__(self, timeout: int, callb: Callable[[], None]):
        self._timeout = timeout
        self._callb = callb
        self._task: asyncio.Task | None = None

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._task = None
        self._callb()

    def start(self) -> None:
        if self._task is None:
            self._task = asyncio.ensure_future(self._job())
        else:
            raise RuntimeError("Timer already started.")

    def cancel(self) -> None:
        if self._task is not None:
            self._task.cancel()
            self._task = None


class Asyncio_timer_factory(Timer_factory):
    def create_timer(self, timeout: int, callb: Callable[[], None]) -> Timer:
        return Asyncio_timer(timeout, callb)
