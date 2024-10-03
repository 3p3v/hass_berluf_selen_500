# %%
from dataclasses import dataclass
from typing import Callable
from .intf import Device_buildable_intf


@dataclass
class Serial_conf:
    com: str = "COM0"
    baud_rate: int = 9600
    stop_bits: int = 1
    char_size: int = 8
    parity: str = "N"


# %%
class Device_serial_intf_builder:
    def create_intf(
        self,
        connect_callb: Callable[[], None],
        disconnect_callb: Callable[[Exception | None], None],
        conf: Serial_conf,
    ) -> Device_buildable_intf:
        raise NotImplementedError()
