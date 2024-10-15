from typing import Callable
from .func import Invokable_func, Observer_func


class Callb_store:  # TODO find some more efficient way to store callbacks, FIXME run callback one time, instead of multiple times
    """Class for storing callbacks for specyfied addresses."""

    def __init__(self) -> None:
        self._callbs: dict[int, list[tuple[int, Observer_func]]] = {}

    def add_callb(self, addr: int, callb: Observer_func, count: int = 1) -> None:
        """Add a callback."""
        for a in range(addr, addr + count):
            x = self._callbs.get(a)
            if x != None:
                x.append((1, callb))
            else:
                self._callbs[a] = [(1, callb)]

    def add_callb_per_addr(self, addrs: list[int], callb: Observer_func):
        """Add callback for every specyfied address."""
        for a in addrs:
            x = self._callbs.get(a)
            if x != None:
                x.append((1, callb))
            else:
                self._callbs[a] = [(1, callb)]

    def run_callbs(
        self, addr: int, vals: list[int], invoker: Observer_func | None = None
    ) -> None:
        """Run callback for many addressed (from addr to addr + len(vals))."""
        if invoker is None:
            for i, a in enumerate(range(addr, addr + len(vals))):
                x = self._callbs.get(a)
                if x != None:
                    for count, callb in x:
                        callb.callb(a, [vals[i]])  # FIXME
        else:
            for i, a in enumerate(range(addr, addr + len(vals))):
                x = self._callbs.get(a)
                if x != None:
                    for count, callb in x:
                        if callb is not invoker:
                            callb.callb(a, [vals[i]])  # FIXME

    def extend(self, cs) -> None:
        """Extend Callb_store using other object."""
        for a, v in cs._callbs.items():
            x = self._callbs.get(a)
            if x != None:
                x.append(v)
            else:
                self._callbs[a] = v


class Invoke_callb_store:
    """Just run callback."""

    def __init__(self) -> None:
        self._callbs: list[Invokable_func] = []

    def add_callb(self, callb: Invokable_func) -> None:
        """Add a callback."""
        self._callbs.append(callb)

    def run_callbs(self) -> None:
        """Run all callbacks."""
        for c in self._callbs:
            c.callb()
