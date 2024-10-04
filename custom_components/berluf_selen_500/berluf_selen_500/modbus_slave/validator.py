from typing import Callable


class Validator:
    def validate(self, addr: int, val: int) -> None:
        return


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


# %%
class Memory_validator(Validator):
    def __init__(self, addrs: dict[int, Validator_handler]):
        self._addrs = addrs
        return

    def validate(self, addr: int, val: int) -> None:
        a = self._addrs.get(addr)
        if a is not None:
            if not a.validate(val):
                raise RuntimeError(
                    f"Value of the address {addr} can not be equal {val}."
                )

            return
        else:
            raise RuntimeError(f"Address {addr} is inaccessable in this context.")
