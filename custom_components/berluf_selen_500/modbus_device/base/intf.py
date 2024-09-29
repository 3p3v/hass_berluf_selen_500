from typing import Tuple
from modbus_device.base.memory import Memory_rw

# %%
class Slave_builder:
    """ Base class for creating and adding slaves to the interface """
    
    def create_slave(self) -> Tuple[Memory_rw, Memory_rw, Memory_rw, Memory_rw]:
        raise NotImplementedError()

# %%
class Device_intf:
    """ Base for modbus device connectivity interface """
    
    def connect(self) -> bool:
        raise NotImplementedError()
    
    def disconnect(self) -> bool:
        raise NotImplementedError()
    
class Device_buildable_intf(Slave_builder, Device_intf):
    def __init__(self):
        return