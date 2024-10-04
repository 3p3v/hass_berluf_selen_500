import pymodbus
import asyncio

# import serial
from pymodbus.client import ModbusSerialClient as ModbusClient


class Panel:  # TODO make underlying class capable of holding any registry to send and to receive
    def __init__(self, cli: ModbusClient):
        self._addr = 1
        self._cli = cli
        self._01 = 26
        self._02 = 24
        self._03 = 23
        self._04 = 22
        self._05 = 21
        self._ec = 0
        return

    def set_01(self, temp: int):
        self._01 = temp
        return

    def set_02(self, temp: int):
        self._02 = temp
        return

    def set_03(self, temp: int):
        self._03 = temp
        return

    def set_04(self, temp: int):
        self._04 = temp
        return

    def set_05(self, temp: int):
        self._05 = temp
        return

    def set_error(self, ec: str):
        self._ec = int(ec, 2)
        return

    def send_regs(self) -> int:
        self._cli.write_register(258, self._ec, slave=self._addr)
        self._cli.write_register(259, self._01, slave=self._addr)
        self._cli.write_register(260, self._02, slave=self._addr)
        self._cli.write_register(261, self._03, slave=self._addr)
        self._cli.write_register(262, self._04, slave=self._addr)
        self._cli.write_register(263, self._05, slave=self._addr)
        print("WRITE")
        return 0

    def receive_holding_regs(self):  # for now ignore values
        print(
            f"0:   {self._cli.read_holding_registers(0, 11, slave=self._addr).registers}"
        )
        print(
            f"60:  {self._cli.read_holding_registers(60, 13, slave=self._addr).registers}"
        )
        print(
            f"275: {self._cli.read_holding_registers(274, 5, slave=self._addr).registers}"
        )
        return


async def main():
    while True:
        cli = ModbusClient(
            port="/dev/pts/4", baudrate=9600, bytesize=8, parity="N", stopbits=1
        )

        panel = Panel(cli)

        # panel.receive_holding_regs()

        panel.set_error("00000000")
        panel.send_regs()

        panel.receive_holding_regs()

        cli.close()
        # await asyncio.sleep(10)


asyncio.run(main())
