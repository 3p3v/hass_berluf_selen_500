"""Memorie's base function classes and base functions."""

from typing import Callable, override

from .memory import Memory
from .timer import Timer_factory


# %%
class Device_func:
    """Base class for some functionality of a device."""


class Invokable_func(Device_func):
    """Class observing if something was invoked."""

    def callb(self) -> None:
        """Run a callback when some state changes."""
        raise NotImplementedError()


class Observer_func(Device_func):
    """Class observing changes in addresses."""

    def callb(self, addr: int, vals: list[int]) -> None:
        """Run a callback when the value of an observed address changes."""
        raise NotImplementedError()


class Timeout_manager(Invokable_func):
    """Checks if connection between master and slave is active."""

    def __init__(
        self,
        memory: Memory,
        timer_factory: Timer_factory,
        timeout: int,
        reset_callb: Callable[[], None],
        callb: Callable[[], None],
    ):
        self._usr_callb = callb
        self._usr_reset_callb = reset_callb
        self._timer = timer_factory.create_timer(timeout, self._fail_callb)
        memory.get_invoke_callb_service().add_callb(self)

    @override
    def callb(self) -> None:
        self._timer.cancel()
        self._usr_reset_callb()
        self._timer.start()

    def _fail_callb(self) -> None:
        self._usr_callb()
        self._timer.start()

    def start(self) -> None:
        """Start timeout manager."""
        self._timer.start()

    def cancel(self) -> None:
        """Stop timeout manager."""
        self._timer.cancel()


# TODO make next timeout manager that checks bool for activity every second


class Collective_persistant(Observer_func):
    """Save all specyfied addresses' variables."""

    def __init__(self, memory: Memory, addrs: list[int]) -> None:
        memory.get_callb_service().add_callb_per_addr(addrs, self)

    @override
    def callb(self, addr: int, vals: list[int]) -> None:
        self._save()

    def _save(self) -> None:
        """Save all addresses implementation."""
        raise NotImplementedError()
