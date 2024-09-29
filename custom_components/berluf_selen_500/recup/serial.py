from typing import Tuple
from modbus_device.base.intf import Device_buildable_intf
from modbus_device.base.serial import (Serial_conf, Device_serial_intf_builder)
from modbus_device.base.memory import Memory_rw

# %%
class Recup_serial_intf(Device_buildable_intf): # TODO 
    """ Sets up an interface for the recuperator """
    
    def __init__(self, com: str, impl_builder: Device_serial_intf_builder):
        self._impl = impl_builder.create_intf(Serial_conf(com, 9600, 1, 8, "O"))
        return
        
    def create_slave(self) -> Tuple[Memory_rw, Memory_rw, Memory_rw, Memory_rw]:
        return self._impl.create_slave()
    
    async def connect(self):
        return await self._impl.connect()
    
    def disconnect(self) -> bool:
        return self._impl.disconnect()