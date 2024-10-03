class Validator:
    def validate(self, addr: int) -> None:
        return

# %%
class Memory_validator(Validator):
    def __init__(self, addrs: list):
        self._addrs = addrs
        return
    
    def validate(self, addr: int) -> None:
        if (addr in self._addrs):
            return
        else:
            raise RuntimeError(f"Address {addr} is inaccessable in this context.")    