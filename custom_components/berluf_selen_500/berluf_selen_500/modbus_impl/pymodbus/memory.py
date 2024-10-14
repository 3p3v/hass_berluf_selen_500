from typing import override
from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.validator import (
    Setter_validator,
    Validator,
)
from ...modbus_slave.memory import Memory_rw
from ...modbus_slave.callb import Callb_store
from pymodbus.datastore import ModbusSparseDataBlock


# %%
class Pymodbus_memory(Memory_rw, ModbusSparseDataBlock):  # TODO change to proxy
    """Memory implementation using pymodbus."""

    def __init__(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ):
        Memory_rw.__init__(self, validator, setter_validator, callbs)
        ModbusSparseDataBlock.__init__(self)

        # Set memory
        for a, v in mem.items():
            self._set_multi_val(a, v)

        return

    def _get_single_val(self, addr: int) -> int:
        return self.getValues(addr, 1)[0]  # TODO

    def _set_single_val(self, addr: int, val: int) -> None:
        self.setValues(addr, [val])  # TODO
        return

    def _set_multi_val(self, addr: int, val: list) -> None:
        self.setValues(addr, val)  # TODO
        return

    @override
    def get_all_single_vals(self) -> dict[int, int]:
        return self.values

    def setValues(self, address, vals):
        """Set the requested values of the datastore."""
        super().setValues(address, vals)
        # Run callbacks
        self._callbs.run_callbs(address, vals)
        return

    def validate(self, address, count=1):
        """Check to see if the request is in range."""
        # result = super().validate(address, count=count)

        result = True  # FIXME
        if result:
            # Check again but with validator this time
            try:
                self._validator.validate(address, count)  # TODO DELETE
            except:
                # Violation
                result = False

        return result
