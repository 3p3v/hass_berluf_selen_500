from typing import Callable, List
from .validator import (
    Memory_validator,
    Setter_validator,
    Validator,
    Validator_handler,
)
from .callb import Callb_store


# %%
class Memory:
    """Represents a Modbus memory fragment"""

    def __init__(
        self,
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ):
        self._validator = validator
        self._callbs = callbs
        self._setter_validator = setter_validator
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

    def _set_single_val_intf(self, addr: int, val: int) -> None:
        self._setter_validator.validate_val(addr, val)
        self._set_single_val_intf(addr, val)

    def _set_multi_val_intf(self, addr: int, val: list[int]) -> None:
        self._setter_validator.validate_vals(addr, val)
        self._set_multi_val_intf(addr, val)

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
        def __init__(self, impl, validator: Validator) -> None:
            self._impl = impl
            self._validator = validator

        def set_single_val(self, addr: int, val: int) -> None:
            self._validator.validate(addr)
            self._impl._set_single_val(addr, val)
            return

        def set_multi_val(self, addr: int, val: List[int]) -> None:
            self._validator.validate(addr)
            self._impl._set_multi_val(addr, val)
            return

        def update_handler(self, addr: int, handler: Validator_handler):
            self._impl._setter_validator.update_handler(addr, handler)
            return

        def update(self, setter):
            self._validator.update(setter._validator)

    def __init__(
        self,
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ):
        super().__init__(validator, setter_validator, callbs)
        self._settable_addrs = setter_validator.get_address_list()
        return

    def get_setter(
        self, addr_valids: dict[int, list[Validator_handler]]
    ) -> Memory_setter:
        # Check if all addrs exist
        all_addrs = []
        for addrs, valids in addr_valids.items():
            all_addrs.extend(range(addrs, len(valids)))

        if not all(a in self._settable_addrs for a in all_addrs):
            raise RuntimeError("Specyfied unsettable values.")

        # Update validators
        offset = 0
        for valids in addr_valids.values():
            for a, v in zip(all_addrs[offset:], valids):
                self._settable_addrs.remove(a)
                self._setter_validator.update_handler(a, v)

            offset += len(valids)

        return Memory_rw.Memory_setter(self, Memory_validator(all_addrs))

    def get_setter_unsafe(self, addrs: list[int]) -> Memory_setter:
        return Memory_rw.Memory_setter(self, Memory_validator(addrs))

    def clean_up(self, raise_warning: bool = True) -> None:
        """Clean up after initializing all functions."""
        # Show warinigs
        if raise_warning:
            if len(self._settable_addrs) != 0:
                raise Warning("Not all addresses have been distributed.")

        # Clean up
        self._settable_addrs.clear()
        return
