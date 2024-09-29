from modbus_device.base.memory import Memory_rw_initializer
from modbus_device.base.callb import Callb_store
from pymodbus.datastore import ModbusSparseDataBlock

# %%
class Pymodbus_memory(Memory_rw_initializer, ModbusSparseDataBlock): # TODO change to proxy
    """ Memory implementation using pymodbus """
    
    def __init__(self):
        Memory_rw_initializer.__init__(self)
        ModbusSparseDataBlock.__init__(self)
        # super(Pymodbus_memory, self).__init__()
        
        self._callbs: Callb_store = Callb_store()
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
        
        result = True # FIXME
        if (result):
            # Check again but with validator this time
            try:
                self._validator_rw.validate(address)
            except:
                # Violation
                result = False
        
        return result