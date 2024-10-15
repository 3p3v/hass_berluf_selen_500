from .func import Observer_func
from .validator import (
    Memory_validator,
    Setter_validator,
    Validator,
    Validator_handler,
)
from .callb import Callb_store, Invoke_callb_store


# %%
class Memory:
    """Represents a Modbus memory fragment."""

    def __init__(
        self,
        validator: Validator,
        setter_validator: Setter_validator,
        master_validator: Validator,
        master_setter_validator: Setter_validator,
        callbs: Callb_store,
        invoke_callbs: Invoke_callb_store,
    ) -> None:
        # Validate self getter
        self._validator = validator
        # Validate self setter
        self._setter_validator = setter_validator
        # Validate master getter
        self._master_validator = master_validator
        # Validate master setter
        self._master_setter_validator = master_setter_validator
        # Callbacks to run when value changes
        self._callbs = callbs
        # Callbacks to run when received data from master
        self._invoke_callbs = invoke_callbs
        return

    def _get_single_val(self, addr: int) -> int:
        raise NotImplementedError()

    def _get_multi_val(self, addr: int, count: int) -> list[int]:
        raise NotImplementedError()

    def get_single_val(self, addr: int) -> int:
        """Get single registry."""
        self._validator.validate(addr)
        return self._get_single_val(addr)

    def _set_single_val(
        self, addr: int, val: int, invoker: Observer_func | None
    ) -> None:
        raise NotImplementedError()

    def _set_multi_val(
        self, addr: int, val: list[int], invoker: Observer_func | None
    ) -> None:
        raise NotImplementedError()

    def _set_single_val_intf(
        self, addr: int, val: int, invoker: Observer_func | None
    ) -> None:
        self._setter_validator.validate_val(addr, val)
        if self._get_single_val(addr) != val:
            self._set_single_val(addr, val, invoker)
            self._callbs.run_callbs(addr, [val])

    def _set_multi_val_intf(
        self, addr: int, val: list[int], invoker: Observer_func | None
    ) -> None:
        self._setter_validator.validate_vals(addr, val)
        self._set_multi_val(addr, val, invoker)
        for a, v, o in zip(
            range(addr, addr + len(val)), val, self._get_multi_val(addr, len(val))
        ):
            if v != o:
                self._callbs.run_callbs(a, [v])

    def get_callb_service(self) -> Callb_store:
        """Get callback service used for callbacks running when registry value changes."""
        return self._callbs

    def get_invoke_callb_service(self) -> Invoke_callb_store:
        """Get callback service used for callbacks running when registry value changes."""
        return self._invoke_callbs

    def get_address_list(self) -> list[int]:
        """List all addresses managed by this memory."""
        return self._validator.get_address_list()

    def get_all_single_vals(self) -> dict[int, int]:
        """Retreive values from memory."""
        raise NotImplementedError()

    def get_all_single_sorted_vals(self) -> list[tuple[int, int]]:
        """Retreive values from memory, sorted by key."""
        return sorted(self.get_all_single_vals().items())

    def get_all_multi_vals(self) -> dict[int, list[int]]:
        """Retreive values from memory in a more friendly form."""
        single_vals = self.get_all_single_sorted_vals()

        if len(single_vals) > 0:
            # Algh
            addr = single_vals[0][0]
            offset = 1
            val_list = [single_vals[0][1]]
            # Return var
            multi_vals = {addr: val_list}
            # Algh
            for a, v in single_vals[1:]:
                if a == addr + offset:
                    val_list.append(v)
                    offset += 1
                else:
                    val_list = [v]
                    multi_vals[a] = val_list
                    addr = a
                    offset = 1

            return multi_vals
        else:
            return {}


class Memory_rw(Memory):
    """Represents a Modbus readable/writeable memory (readable by masster)."""

    class Memory_setter:
        """Class returned when a function registes for setting variables."""

        def __init__(self, impl: Memory, validator: Validator) -> None:
            self._impl = impl
            # Validator checking if a function has a right to change the specyfied address
            self._validator = validator

        def set_single_val(
            self, addr: int, val: int, invoker: Observer_func | None = None
        ) -> None:
            """Change single registry."""
            self._validator.validate(addr)
            self._impl._set_single_val_intf(addr, val, invoker)
            return

        def set_multi_val(
            self, addr: int, val: list[int], invoker: Observer_func | None = None
        ) -> None:
            """Change many continous registries."""
            self._validator.validate(addr)
            self._impl._set_multi_val_intf(addr, val, invoker)
            return

        def update_handler(self, addr: int, handler: Validator_handler) -> None:
            """Update setting validation."""
            self._impl._setter_validator.update_handler(addr, handler)
            return

        def update(self, setter) -> None:
            """Update a whole setter."""
            self._validator.update(setter._validator)

    def __init__(
        self,
        validator: Validator,
        setter_validator: Setter_validator,
        master_validator: Validator,
        master_setter_validator: Setter_validator,
        callbs: Callb_store,
        invoke_callbs: Invoke_callb_store,
    ):
        super().__init__(
            validator,
            setter_validator,
            master_validator,
            master_setter_validator,
            callbs,
            invoke_callbs,
        )
        # List for tracking addresses managed by functions
        self._settable_addrs = setter_validator.get_address_list()
        return

    def get_setter(
        self, addr_valids: dict[int, list[Validator_handler]]
    ) -> Memory_setter:
        """Register a function for setting variables by getting a setter object."""
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

    def clean_up(self) -> None:
        """Clean up after initializing all functions."""
        # Show warinigs
        if len(self._settable_addrs) != 0:
            raise Warning("Not all addresses have been distributed.")

        # Clean up
        self._settable_addrs.clear()
        return
