from modbus_device.base.memory import (Memory_rw, Memory_rw_initializer)
from modbus_device.base.device import Device
from modbus_device.base.intf import Slave_builder
from modbus_device.base.persistant import (Memory_persistant, Memory_persistant_factory)
from modbus_device.base.validator import Memory_validator
from modbus_device.base.callb import Callb_store

# %%
class Recup_device(Device):
    def __init__(self, impl_builder: Slave_builder, persistant_factory: Memory_persistant_factory):
        # self._impl_builder: Impl_builder = impl_builder
        self._persistant_factory: Memory_persistant_factory = persistant_factory
        
        (_, _, self.holding_registers, _) = impl_builder.create_slave()
        self.coils = None
        self.discrete_inputs = None
        self.input_registers = None
        self._create_device()
        return
    
    def _get_valid_mem(self, reg_mem: dict, callbs: Callb_store, persistant: Memory_persistant) -> list:
        # Set valid addresses and persistant
        valid_mem = []
        for a, v in reg_mem.items(): # TODO move to try: except:
            len_ = len(v)
            # Validator
            valid_mem.extend(range(a, a + len_))
            # Persistant
            callbs.add_callb(a, lambda addr, vals: persistant.save(addr, vals), len_)
            
        return valid_mem
    
    def _create_memory(self, mem: Memory_rw_initializer, reg_mem_r: dict, reg_mem_rw: dict, persistant: Memory_persistant) -> Memory_rw: # TODO accept only Memory_rw or return configured validator and persistant 
        try:
            reg_mem = persistant.load()
        except:
            # Set runtime memory
            reg_mem = {}
            reg_mem.update(reg_mem_r)
            reg_mem.update(reg_mem_rw)
            
            # Save default values to persistant
            for a, v in reg_mem.items():
                persistant.save(a, v)

        # Set memory
        mem.set_memory(reg_mem)
        
        callbs = Callb_store()
        
        # Get valid addresses and persistant for registers writable by device itself
        valid_mem_r = self._get_valid_mem(reg_mem_r, callbs, persistant)
        
        # Get valid addresses and persistant for registers writable by master
        valid_mem_rw = self._get_valid_mem(reg_mem_rw, callbs, persistant)
        valid_mem_rw.extend(valid_mem_r)
        
        # Set valid addresses
        mem.set_callb_service(callbs)
        mem.set_validator_service(Memory_validator(valid_mem_r), Memory_validator(valid_mem_rw))
        return mem     
    
    def _create_device(self):
        holding_registers_persistant = self._persistant_factory.create_persistant("holding_registers") 
        holding_registers_mem_r = {
            0: [1, 0, 25, 18, 18, 26, 22, 5, 60, 60, 30],
            60: [2, 25, 0, 24, 1, 0, 25, 25, 25, 0, 10, 10, 2],
            274: [26, 3, 112, 0, 16]
        }
        holding_registers_mem_rw = {
            258: [128, 20, 20, 20, 20, 20]
        }
        self._create_memory(self.holding_registers, holding_registers_mem_r, holding_registers_mem_rw, holding_registers_persistant)
        
        return