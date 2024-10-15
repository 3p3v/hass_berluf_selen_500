from typing import override
from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.validator import (
    Setter_validator,
    Validator,
)
from ...modbus_slave.memory import Memory_rw
from ...modbus_slave.callb import Callb_store, Invoke_callb_store
from pymodbus.datastore import ModbusSparseDataBlock


# %%
class Pymodbus_memory(Memory_rw, ModbusSparseDataBlock):  # TODO change to proxy
    """Memory implementation using pymodbus."""

    def __init__(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        master_validator: Validator,
        master_setter_validator: Setter_validator,
        callbs: Callb_store,
        invoke_callbs: Invoke_callb_store,
    ):
        Memory_rw.__init__(
            self,
            validator,
            setter_validator,
            master_validator,
            master_setter_validator,
            callbs,
            invoke_callbs,
        )
        ModbusSparseDataBlock.__init__(self)

        # Set memory
        for a, v in mem.items():
            self._set_multi_val(a, v)

        return

    @override
    def _get_single_val(self, addr: int) -> int:
        return self.values[addr]

    @override
    def _get_multi_val(self, addr: int, count: int) -> list[int]:
        return [self.values[a] for a in range(addr, addr + count)]

    @override
    def _set_single_val(self, addr: int, val: int) -> None:
        self.values[addr] = val
        return

    @override
    def _set_multi_val(self, addr: int, val: list) -> None:
        for a, v in zip(range(addr, addr + len(val)), val):
            self.values[a] = v

        return

    @override
    def get_all_single_vals(self) -> dict[int, int]:
        return self.values

    @override
    def setValues(self, address, vals):
        """Set the requested values of the datastore."""
        self._master_setter_validator.validate_vals(address, vals)
        super().setValues(address, vals)
        # Run callbacks
        self._callbs.run_callbs(address, vals)
        return

    @override
    def getValues(self, address, count=1):
        """Set the requested values of the datastore."""
        self._master_validator.validate(address)
        return super().getValues(address, count)

    @override
    def validate(self, address, count=1):
        """Check to see if the request is in range."""
        res = super().validate(address, count=count)
        if res:
            self._invoke_callbs.run_callbs()

        return res
