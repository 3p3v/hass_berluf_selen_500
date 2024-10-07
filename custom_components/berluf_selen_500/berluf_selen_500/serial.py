from ast import Call
from typing import Tuple, override
from typing import Callable

from .modbus_slave.callb import Callb_store
from .modbus_slave.validator import Setter_validator, Validator
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

    @override
    def create_coils(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        self._coils = self._impl.create_coils(mem, validator, setter_validator, callbs)

    @override
    def create_discrete_inputs(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        self._discrete_inputs = self._impl.create_discrete_inputs(
            mem, validator, setter_validator, callbs
        )

    @override
    def create_holding_registers(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        self._holding_registers = self._impl.create_holding_registers(
            mem, validator, setter_validator, callbs
        )

    @override
    def create_input_registers(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        self._input_registers = self._impl.create_input_registers(
            mem, validator, setter_validator, callbs
        )

    @override
    def create_slave(self) -> Tuple[Memory_rw, Memory_rw, Memory_rw, Memory_rw]:
        return self._impl.create_slave()

    async def connect(self) -> None:
        await self._impl.connect()

    async def disconnect(self) -> None:
        await self._impl.disconnect()
