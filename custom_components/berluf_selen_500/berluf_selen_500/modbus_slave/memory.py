from typing import Callable, List
from .validator import (
    Memory_validator,
    Setter_validator,
    Setter_validator_addr_distributor,
    Validator,
    Validator_handler,
)
from .callb import Callb_store


# %%
class Memory:
    """Represents a Modbus memory fragment"""

    def __init__(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        callbs: Callb_store,
    ):
        self._validator = validator
        self._callbs = callbs

        for a, v in mem.items():
            self._set_multi_val(a, v)

        return

    def _get_single_val(self, addr: int) -> int:
        raise NotImplementedError()

    def get_single_val(self, addr: int) -> int:
        self._validator.validate(addr)
        return self._get_single_val(addr)

    def _set_single_val(self, addr: int, val: int) -> None:
        raise NotImplementedError()

    def _set_multi_val(self, addr: int, val: list[int]) -> None:
        raise NotImplementedError()

    def set_change_callb(
        self, addr: int, callb: Callable[[int, list], None], count: int = 1
    ) -> None:  # TODO DELETE
        self._callbs.add_callb(addr, callb, count)
        return

    def get_callb_service(self) -> Callb_store:
        return self._callbs

    def get_address_list(self) -> list[int]:
        return self._validator.get_address_list()


# class Memory_r(Memory):
#     """Represents a Modbus readable memory (readable/writable by master)"""

#     def __init__(self):
#         super().__init__()
#         return


class Memory_rw(Memory):
    """Represents a Modbus readable/writeable memory (readable by masster)"""

    class Memory_setter:
        def __init__(
            self,
            impl,
            validator: Setter_validator,
        ) -> None:
            self._impl = impl
            self._validator = validator

        def set_single_val(self, addr: int, val: int) -> None:
            self._validator.validate_vals(addr, [val])
            self._impl._set_single_val(addr, val)
            return

        def set_multi_val(self, addr: int, val: List[int]) -> None:
            self._validator.validate_vals(addr, val)
            self._impl._set_multi_val(addr, val)
            return

    def __init__(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator_distributor: Setter_validator_addr_distributor,
        callbs: Callb_store,
    ):
        super().__init__(mem, validator, callbs)
        self._setter_validator_distributor = setter_validator_distributor
        return

    def get_setter(self, addrs: dict[int, list[Validator_handler]]) -> Memory_setter:
        return Memory_rw.Memory_setter(
            self, self._setter_validator_distributor.get_setter(addrs)
        )
