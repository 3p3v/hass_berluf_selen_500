from ...modbus_slave.timer import Timer, Timer_factory
import asyncio
from typing import Callable


class Asyncio_timer(Timer):
    def __init__(self, timeout: int, callb: Callable[[], None]):
        self._timeout = timeout
        self._callb = callb
        self._task: asyncio.Task | None = None
        # If cancellation procedure was called
        self._cancel_in_progress = False
        # Should be running
        self._is_on = False

    async def _job(self) -> None:  # Implement separate stop job
        if not self._cancel_in_progress and self._is_on:
            await asyncio.sleep(self._timeout)
        else:
            self._task = None
            await self._stop_job()
            return

        if not self._cancel_in_progress and self._is_on:
            self._task = None
            self._is_on = False
            self._callb()
        else:
            self._task = None
            self._is_on = False
            await self._stop_job()
            return

    async def _stop_job(self):
        # Do not cancel if called from _job procedure
        if self._task is not None:
            self._task.cancel()
            # Wait untill cancelled
            while not self._task.cancelled():
                await asyncio.sleep(0)

            self._task = None

        # Start timer again if user requested in the meanwhile (pending start if _if_on but the task was not started)
        if self._is_on is True:
            self._task = asyncio.ensure_future(self._job())

        self._cancel_in_progress = False

    def start(self) -> None:
        if self._is_on is False:
            # Mark as turned on so can be cancelled
            self._is_on = True
            # Check if cancellation already in progress (task will be started in the stop procedure)
            if self._cancel_in_progress is False:
                self._task = asyncio.ensure_future(self._job())
        else:
            raise RuntimeError("Timer already started.")

    def cancel(self) -> None:
        if self._is_on is True:
            # Mark as turned off
            self._is_on = False
            # Check if really started
            if self._task is not None and self._cancel_in_progress is False:
                # Mark as cancell in progress
                self._cancel_in_progress = True
                # Unmark start
                asyncio.ensure_future(self._stop_job())
        else:
            raise RuntimeError("Timer hasn't started yet.")


class Asyncio_timer_factory(Timer_factory):
    def create_timer(self, timeout: int, callb: Callable[[], None]) -> Timer:
        return Asyncio_timer(timeout, callb)
