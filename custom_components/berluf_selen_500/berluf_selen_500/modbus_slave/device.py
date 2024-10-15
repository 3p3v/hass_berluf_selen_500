from dataclasses import dataclass
from .memory import Memory_rw  # , Memory_r


@dataclass
class Device:
    """Represents a Modbus device's full memory."""

    coils: Memory_rw
    discrete_inputs: Memory_rw
    holding_registers: Memory_rw
    input_registers: Memory_rw
