from typing import Callable

from .memory import Memory
from .persistant import Memory_persistant
from .device import Device
from .timer import Timer_factory


# %%
class Device_func:
    """Base class for some functionality of a device"""

    def __init__(self, device: Device) -> None:
        self._device: Device = device


class Persistant_saver:
    """Saves new values to persistant."""

    def enable_persistant(
        self,
        memory: Memory,
        persistant: Memory_persistant,
    ):
        self._persistant = persistant
        memory.get_callb_service().add_callb_per_addr(
            memory.get_address_list(),
            lambda addr, vals: persistant.save(addr, vals),
        )


class Timeout_manager:
    """Checks if connection between master and slave is active."""

    def __init__(
        self,
        memory: Memory,
        addrs: list[int],
        timer_factory: Timer_factory,
        timeout: int,
        reset_callb: Callable[[], None],
        callb: Callable[[], None],
    ):
        self._usr_callb = callb
        self._usr_reset_callb = reset_callb
        self._timer = timer_factory.create_timer(timeout, self._fail_callb)
        memory.get_callb_service().add_callb_per_addr(addrs, self._callb)

    def _callb(self, addr: int, vals: list[int]) -> None:
        self._timer.cancel()
        self._usr_reset_callb()
        self._timer.start()

    def _fail_callb(self) -> None:
        self._usr_callb()
        self._timer.start()

    def start(self) -> None:
        self._timer.start()

    def cancel(self) -> None:
        self._timer.cancel()


# TODO make next timeout manager that checks bool for activity every second
