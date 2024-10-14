# %%
from .memory import Memory


class Memory_persistant:
    # def load(self) -> dict[int, list[int]]:
    #     raise NotImplementedError()

    def save_single(self, addr: int, val: int) -> None:
        raise NotImplementedError()

    def save(self, addr: int, vals: list[int]) -> None:
        raise NotImplementedError()

    def save_all(self, all: dict[int, list[int]]) -> None:
        raise NotImplementedError()


# %%
class Memory_persistant_factory:
    def create_persistant(self, subfile: str) -> None:
        raise NotImplementedError()


# %%
class Persistant_dummy(Memory_persistant):
    def __init__(self, subfile: str) -> None:
        self._mem = dict[str, dict[int, int]]()
        self._subfile = subfile
        self._mem[self._subfile] = dict[int, int]()

    # def load(self) -> dict:
    #     raise NotImplementedError()

    def save_single(self, addr: int, val: int) -> None:
        self._mem[self._subfile][addr] = val

    def save(self, addr: int, vals: list[int]) -> None:
        for a, v in zip(range(addr, addr + len(vals)), vals):
            self._mem[self._subfile][a] = v


class Collective_persistant:
    def save(self) -> None:
        raise NotImplementedError()


class Collective_persistant_manager:
    def link(self, memory: Memory, persistant: Collective_persistant) -> None:
        memory.get_callb_service().add_callb_per_addr(
            memory.get_address_list(), lambda a, v: persistant.save()
        )
