from logging import warning

from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.callb import (
    Callb_store,
)
from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.device import (
    Device,
)
from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.memory import (
    Memory_rw,
)
from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.validator import (
    Setter_validator,
    Validator,
)
from ...modbus_slave.intf import Device_buildable_intf
from ...modbus_slave.serial import Serial_conf, Device_serial_intf_builder
from .memory import Pymodbus_memory
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.server import ModbusSerialServer

import asyncio
from asyncio import Event
from typing import Callable, override


class Pymodbus_serial_server(ModbusSerialServer):
    def __init__(
        self,
        connect_callb: Callable[[], None],
        disconnect_callb: Callable[[Exception | None], None],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._disconnect_event = Event()
        self._connect_callb = connect_callb
        self._disconnect_callb = disconnect_callb
        self._task = None

    def callback_connected(self) -> None:
        """Call when connection is succcesfull."""
        self._connect_callb()
        # TODO fix

    def callback_disconnected(self, exc: Exception | None) -> None:
        """Call when connection is lost."""
        self._disconnect_callb(exc)
        self._disconnect_event.set()

    # async def _run_connect(self):
    #     # await self.serve_forever()
    #     try:
    #         await self.serve_forever()
    #     except Exception as ec:
    #         self.callback_disconnected(ec)

    #     self.callback_disconnected(None)

    # async def _wait(self, timeout: int):
    #     await asyncio.sleep(timeout)

    async def run_connect(self):
        if self._task is None:
            self._task = asyncio.ensure_future(self.serve_forever())
            # if self._disconnect_event.is_set():  # TODO FIX
        else:
            raise RuntimeError(f"Could not connect to interface.")

    async def run_disconnect(self):
        if self._task is not None:
            await self.shutdown()  # FIXME
            self._task.cancel()
            self._task = None
        else:
            raise RuntimeError(f"Could not disconnect from interface.")
        # await self._disconnect_event.wait()


# %%
class Pymodbus_serial_intf(Device_buildable_intf):
    def __init__(
        self,
        connect_callb: Callable[[], None],
        disconnect_callb: Callable[[Exception | None], None],
        conf: Serial_conf = Serial_conf(),
    ):
        self._store: dict = {}
        self._i = 1
        self._connect_callb = connect_callb
        self._disconnect_callb = disconnect_callb
        self._conf = conf

        self._reset_memories()
        return

    def _reset_memories(self) -> None:
        self._coils = self._create_memory(
            {}, Validator(), Setter_validator([]), Callb_store()
        )
        self._discrete_inputs = self._create_memory(
            {}, Validator(), Setter_validator([]), Callb_store()
        )
        self._holding_registers = self._create_memory(
            {}, Validator(), Setter_validator([]), Callb_store()
        )
        self._input_registers = self._create_memory(
            {}, Validator(), Setter_validator([]), Callb_store()
        )

    def _create_memory(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> Pymodbus_memory:
        return Pymodbus_memory(mem, validator, setter_validator, callbs)

    @override
    def create_coils(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        self._coils = self._create_memory(mem, validator, setter_validator, callbs)

    @override
    def create_discrete_inputs(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        self._discrete_inputs = self._create_memory(
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
        self._holding_registers = self._create_memory(
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
        self._input_registers = self._create_memory(
            mem, validator, setter_validator, callbs
        )

    @override
    def create_slave(self) -> tuple:
        _discrete_inputs = self._discrete_inputs
        _coils = self._coils
        _input_registers = self._input_registers
        _holding_registers = self._holding_registers
        self._reset_memories()
        self._store[self._i] = ModbusSlaveContext(
            di=_discrete_inputs,
            co=_coils,
            ir=_input_registers,
            hr=_holding_registers,
            zero_mode=True,
        )  # TODO Follow mems pattern

        self._i += 1

        return (
            _coils,
            _discrete_inputs,
            _holding_registers,
            _input_registers,
        )

    @override
    async def connect(self) -> None:
        self._context = ModbusServerContext(slaves=self._store, single=False)
        self._server = Pymodbus_serial_server(
            connect_callb=self._connect_callb,
            disconnect_callb=self._disconnect_callb,
            context=self._context,  # Data storage
            # identity=args.identity,  # server identify
            # timeout=1,  # waiting time for request to complete
            port=self._conf.com,  # serial port
            # custom_functions=[],  # allow custom handling
            # framer=args.framer,  # The framer strategy to use
            stopbits=self._conf.stop_bits,  # The number of stop bits to use
            bytesize=self._conf.char_size,  # The bytesize of the serial messages
            parity=self._conf.parity,  # Which kind of parity to use
            baudrate=self._conf.baud_rate,  # The baud rate to use for the serial device
            # handle_local_echo=False,  # Handle local echo of the USB-to-RS485 adaptor
            # ignore_missing_slaves=True,  # ignore request to a missing slave
            # broadcast_enable=False,  # treat slave_id 0 as broadcast address,
        )
        await self._server.run_connect()
        return

    @override
    async def disconnect(self) -> None:
        await self._server.run_disconnect()
        return


# %%
class Pymodbus_serial_intf_builder(Device_serial_intf_builder):
    def create_intf(
        self,
        connect_callb: Callable[[], None],
        disconnect_callb: Callable[[Exception | None], None],
        conf: Serial_conf,
    ) -> Device_buildable_intf:
        return Pymodbus_serial_intf(connect_callb, disconnect_callb, conf)
