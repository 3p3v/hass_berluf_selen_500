from dataclasses import dataclass
from modbus_device.base.memory import (Memory_r, Memory_rw)

@dataclass
class Device:
    """ Represents a Modbus device's full memory """
    
    coils: Memory_r
    discrete_inputs: Memory_rw
    holding_register: Memory_r
    input_registers: Memory_rw