from typing import (Callable, List)
from modbus_device.base.validator import (Validator)
from modbus_device.base.callb import Callb_store

# %%
class Memory: # TODO init as many members as possible
    """ Represents a Modbus memory fragment """
    def __init__(self, callbs: Callb_store):
        self._callbs: Callb_store = callbs
        return 
    
    def _get_signle_val(self, addr: int) -> int:
        raise NotImplementedError()
    
    def get_single_val(self, addr: int) -> int:
        # self._validator_r.validate(addr)
        return self._get_signle_val(addr)
    
    def set_change_callb(self, addr: int, callb: Callable[[int, list], None], count: int = 1) -> None:
        self._callbs.add_callb(addr, callb, count)
        return

class Memory_r(Memory):
    """ Represents a Modbus readable memory """
    def __init__(self):
        super().__init__()
        return 
    
class Memory_rw(Memory):
    """ Represents a Modbus readable/writeable memory """
    def __init__(self, validator_r: Validator = Validator(), validator_rw: Validator = Validator(), callbs: Callb_store = Callb_store()):
        super().__init__(callbs)
        self._validator_r: Validator = validator_r # TODO make private
        self._validator_rw: Validator = validator_rw
        return 
    
    def _set_single_val(self, addr: int, val: int) -> None:
        raise NotImplementedError()
    
    def _set_multi_val(self, addr: int, val: List[int]) -> None:
        raise NotImplementedError()
    
    def set_single_val(self, addr: int, val: int) -> None:
        self._validator_r.validate(addr)
        self._set_single_val(addr, val)
        return
    
    def set_multi_val(self, addr: int, val: List[int]) -> None:
        self._validator_r.validate(addr)
        self._set_multi_val(addr, val)
        return
    
# %%
class Memory_rw_initializer(Memory_rw): # TODO delete
    """ Initializer for a memory """
    
    def __init__(self):
        super().__init__()
        return
    
    def set_memory(self, mem: dict):
        for a, v in mem.items():
            self.set_multi_val(a, v)
    
    def set_validator_service(self, validator_r: Validator, validator_rw: Validator):
        self._validator_r: Validator = validator_r
        self._validator_rw: Validator = validator_rw
        return
        
    def set_callb_service(self, callbs: Callb_store):
        self._callbs: Callb_store = callbs
        return