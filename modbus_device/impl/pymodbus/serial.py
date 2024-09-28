from modbus_device.base.intf import Device_buildable_intf
from modbus_device.base.serial import (Serial_conf, Device_serial_intf_builder)
from modbus_device.impl.pymodbus.memory import Pymodbus_memory
from pymodbus.datastore import (ModbusSlaveContext, ModbusServerContext)
from pymodbus.server import (StartAsyncSerialServer, StartSerialServer)

# %%
class Pymodbus_serial_intf(Device_buildable_intf):
    def __init__(self, conf: Serial_conf = Serial_conf()):
        self._conf: Serial_conf = conf
        self._store: dict = {}
        return
    
    def _create_memory(self) -> Pymodbus_memory:
        return Pymodbus_memory()
    
    def create_slave(self) -> tuple: 
        # mems = ModbusSlaveContext(self._create_memory(), self._create_memory(), self._create_memory(), self._create_memory())
        # self._store.append(mems) # TODO Follow mems pattern
        # return (mems.store['c'], mems.store['d'], mems.store['h'], mems.store['i'])
        d, c, i, h = self._create_memory(), self._create_memory(), self._create_memory(), self._create_memory()
        self._store[1] = ModbusSlaveContext(di=d, co=c, ir=i, hr=h, zero_mode=True) # TODO Follow mems pattern
        return (c, d, h, i)
        
    async def connect(self) -> bool:
        self._context = ModbusServerContext(slaves=self._store, single=False)
        self._server = await StartAsyncSerialServer(
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
        return

    async def disconnect(self) -> bool:
        await self._server.close()
        return
    
# %%
class Pymodbus_serial_intf_builder(Device_serial_intf_builder):
    def create_intf(self, conf: Serial_conf) -> Device_buildable_intf:
        return Pymodbus_serial_intf(conf)