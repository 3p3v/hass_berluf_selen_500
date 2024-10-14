from typing import Callable, override

from dataclasses import dataclass


class Validator:
    def validate(self, addr: int, count: int = 1) -> None:
        raise NotImplementedError()

    def get_address_list(self) -> list[int]:
        raise NotImplementedError()

    def update(self, validator) -> None:
        raise NotImplementedError()


class Validator_handler:
    def validate(self, val: int) -> bool:
        raise NotImplementedError()


class Equal_handler(Validator_handler):
    """Return true if values are equal."""

    def __init__(self, val_eq: int) -> None:
        self._val_eq = val_eq

    @override
    def validate(self, val: int) -> bool:
        return val == self._val_eq


class One_of_handler(Validator_handler):
    """Return true if values are equal."""

    def __init__(self, val_eq: list[int]) -> None:
        self._val_eq = val_eq

    @override
    def validate(self, val: int) -> bool:
        return val in self._val_eq


class Smaller_handler(Validator_handler):
    """Return true if given value is smaller."""

    def __init__(self, val_big: int) -> None:
        self._val_big = val_big

    @override
    def validate(self, val: int) -> bool:
        return val < self._val_big


class Bigger_equal_handler(Smaller_handler):
    def __init__(self, val_small: int) -> None:
        super().__init__(val_small)

    @override
    def validate(self, val: int) -> bool:
        return super().validate(val)


class Bigger_handler(Validator_handler):
    """Return true if given value is smaller."""

    def __init__(self, val_small: int) -> None:
        self._val_small = val_small

    @override
    def validate(self, val: int) -> bool:
        return val > self._val_small


class Smaller_equal_handler(Smaller_handler):
    def __init__(self, val_big: int) -> None:
        super().__init__(val_big)

    @override
    def validate(self, val: int) -> bool:
        return super().validate(val)


class Many_handler(Validator_handler):
    def __init__(self, valids: list[Validator_handler]) -> None:
        self._valids = valids
        return

    @override
    def validate(self, val: int) -> bool:
        return all(x.validate(val) for x in self._valids)


class None_validator(Validator_handler):
    @override
    def validate(self, val: int) -> bool:
        return False


class Memory_validator(Validator):
    def __init__(self, addrs: list) -> None:
        self._addrs = addrs
        return

    @override
    def validate(self, addr: int, count: int = 1) -> None:
        for a in range(addr, count):
            if a in self._addrs:
                return
            else:
                raise RuntimeError(f"Address {a} is inaccessable in this context.")

    @override
    def get_address_list(self) -> list[int]:
        return self._addrs

    @override
    def update(self, validator) -> None:
        self._addrs.extend(validator.get_address_list())


# %%
class Setter_validator(Validator):
    # def __init__(self, addr_valids: dict[int, list[Validator_handler]]) -> None:
    def __init__(self, addr: list[int]) -> None:
        self._addrs: dict[int, Validator_handler] = {}
        # Add vallidators one by one
        for a in addr:
            # One validator for each adddress
            self._addrs[a] = None_validator()

        return

    @override
    def validate(self, addr: int, count: int = 1) -> None:
        for a in range(addr, count):
            if a in self._addrs:
                return
            else:
                raise RuntimeError(f"Address {a} is inaccessable in this context.")

    @override
    def get_address_list(self) -> list[int]:
        return list(self._addrs.keys())

    @override
    def update(self, validator) -> None:
        for a in validator.get_address_list():
            if self._addrs.get(a) is None:
                self._addrs[a] = None_validator()

    def validate_val(self, addr: int, val: int) -> None:
        self.validate_vals(addr, [val])

    def validate_vals(self, addr: int, val: list[int]) -> None:
        for a, v in zip(range(addr, len(val)), val):
            ar = self._addrs.get(a)
            if ar is not None:
                if not ar.validate(v):
                    raise RuntimeError(
                        f"Value of the address {addr} can not be equal {v}."
                    )

                return
            else:
                raise RuntimeError(f"Address {addr} is inaccessable in this context.")

    def update_handler(self, addr: int, handler: Validator_handler) -> None:
        try:
            self._addrs[addr] = handler
        except:
            raise RuntimeError(f"Element {addr} is not under validation in this unit.")


# class Setter_validator_addr_distributor:
#     def __init__(self, addrs: list[int]) -> None:
#         self._addrs = addrs

#     def _addr_dict_to_list(
#         self, addr_valids: dict[int, list[Validator_handler]]
#     ) -> list[int]:
#         addrs = []
#         for a, v in addr_valids.items():
#             addrs.extend(range(a, len(v)))

#         return addrs

#     def _remove_from_available(self, addrs: list[int]) -> None:
#         for a in addrs:
#             self._addrs.remove(a)

#     def get_setter(
#         self, addr_valids: dict[int, list[Validator_handler]]
#     ) -> Setter_validator:
#         """Get setter validator with checking if address is already owned."""
#         # Get all addrs
#         addrs = self._addr_dict_to_list(addr_valids)

#         # Check if values exist
#         if all(a in self._addrs for a in addrs):
#             # Remove from available
#             self._remove_from_available(addrs)

#             return Setter_validator(addr_valids)
#         else:
#             raise RuntimeError("Invalid addresses specyfied.")

#     def get_setter_unsafe(
#         self, addr_valids: dict[int, list[Validator_handler]]
#     ) -> Setter_validator:
#         """Get setter validator WITHOUT checking if address is already owned."""
#         return Setter_validator(addr_valids)
