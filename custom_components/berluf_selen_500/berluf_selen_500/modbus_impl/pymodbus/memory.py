from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.validator import (
    Setter_validator_addr_distributor,
    Validator,
)
from ...modbus_slave.memory import Memory_rw
from ...modbus_slave.callb import Callb_store
from pymodbus.datastore import ModbusSparseDataBlock


# %%
class Pymodbus_memory(Memory_rw, ModbusSparseDataBlock):  # TODO change to proxy
    """Memory implementation using pymodbus"""

    def __init__(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator_distributor: Setter_validator_addr_distributor,
        callbs: Callb_store,
    ):
        Memory_rw.__init__(self, mem, validator, setter_validator_distributor, callbs)
        ModbusSparseDataBlock.__init__(self)
        # super(Pymodbus_memory, self).__init__()
        return

    def _get_single_val(self, addr: int) -> int:
        return self.getValues(addr, 1)[0]

    def _set_single_val(self, addr: int, val: int) -> None:
        self.setValues(addr, [val])
        return

    def _set_multi_val(self, addr: int, val: list) -> None:
        self.setValues(addr, val)
        return

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
                self._validator.validate(address, count)
            except:
                # Violation
                result = False

        return result
