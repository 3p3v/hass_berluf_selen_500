from typing import Callable

from dataclasses import dataclass


class Validator:
    def validate(self, addr: int, count: int = 1) -> None:
        raise NotImplementedError()

    def get_address_list(self) -> list[int]:
        raise NotImplementedError()


class Validator_handler:
    def validate(self, val: int) -> bool:
        raise NotImplementedError()


class Equal_handler(Validator_handler):
    """Return true if values are equal."""

    def __init__(self, val_eq: int):
        self._val_eq = val_eq

    def validate(self, val: int) -> bool:
        return val == self._val_eq


class One_of_handler(Validator_handler):
    """Return true if values are equal."""

    def __init__(self, val_eq: list[int]):
        self._val_eq = val_eq

    def validate(self, val: int) -> bool:
        return val in self._val_eq


class Smaller_handler(Validator_handler):
    """Return true if given value is smaller."""

    def __init__(self, val_big: int):
        self._val_big = val_big

    def validate(self, val: int) -> bool:
        return val < self._val_big


class Bigger_equal_handler(Smaller_handler):
    def __init__(self, val_small: int):
        super().__init__(val_small)

    def validate(self, val: int) -> bool:
        return super().validate(val)


class Bigger_handler(Validator_handler):
    """Return true if given value is smaller."""

    def __init__(self, val_small: int):
        self._val_small = val_small

    def validate(self, val: int) -> bool:
        return val > self._val_small


class Smaller_equal_handler(Smaller_handler):
    def __init__(self, val_big: int):
        super().__init__(val_big)

    def validate(self, val: int) -> bool:
        return super().validate(val)


class Many_handler(Validator_handler):
    def __init__(self, valids: list[Validator_handler]):
        self._valids = valids
        return

    def validate(self, val: int) -> bool:
        return all(x.validate(val) for x in self._valids)


class None_validator(Validator_handler):
    def validate(self, val: int) -> bool:
        return False


class Memory_validator(Validator):
    def __init__(self, addrs: list):
        self._addrs = addrs
        return

    def validate(self, addr: int, count: int = 1) -> None:
        for a in range(addr, count):
            if a in self._addrs:
                return
            else:
                raise RuntimeError(f"Address {a} is inaccessable in this context.")

    def get_address_list(self) -> list[int]:
        return self._addrs


# %%
class Setter_validator(Validator):
    def __init__(self, addr_valids: dict[int, list[Validator_handler]]):
        self._addrs: dict[int, Validator_handler] = {}
        # Add vallidators one by one
        for addr, valids in addr_valids.items():
            # One validator for each adddress
            for a, v in zip(range(addr, len(valids)), valids):
                self._addrs[a] = v
        return

    def validate(self, addr: int, count: int = 1) -> None:
        for a in range(addr, count):
            if a in self._addrs:
                return
            else:
                raise RuntimeError(f"Address {a} is inaccessable in this context.")

    def get_address_list(self) -> list[int]:
        return list(self._addrs.keys())

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


class Setter_validator_addr_distributor:
    def __init__(self, addrs: list[int]):
        self._addrs = addrs

    def get_setter(
        self, addr_valids: dict[int, list[Validator_handler]]
    ) -> Setter_validator:
        # Get all addrs
        addrs = []
        for a, v in addr_valids.items():
            addrs.extend(range(a, len(v)))

        # Check if values exist
        if all(a in self._addrs for a in addrs):
            # Remove from available
            for a in addrs:
                self._addrs.remove(a)

            return Setter_validator(addr_valids)
        else:
            raise RuntimeError("Invalid addresses specyfied.")
