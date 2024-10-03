from ast import Call
from typing import Tuple
from typing import Callable
from .modbus_slave.intf import Device_buildable_intf
from .modbus_slave.serial import Serial_conf, Device_serial_intf_builder
from .modbus_slave.memory import Memory_rw


# %%
class Recup_serial_intf(Device_buildable_intf):  # TODO
    """Sets up an interface for the recuperator"""

    def __init__(
        self,
        com: str,
        impl_builder: Device_serial_intf_builder,
        connect_callb: Callable[[], None],
        disconnect_callb: Callable[[Exception | None], None],
    ):
        self._impl = impl_builder.create_intf(
            connect_callb, disconnect_callb, Serial_conf(com, 9600, 1, 8, "N")
        )
        return

    def create_slave(self) -> Tuple[Memory_rw, Memory_rw, Memory_rw, Memory_rw]:
        return self._impl.create_slave()

    async def connect(self) -> None:
        await self._impl.connect()

    async def disconnect(self) -> None:
        await self._impl.disconnect()
