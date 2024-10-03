# %%
# !pip3 install pyserial
# !pip3 install pymodbus
# !pip3 install homeassistant


# %%
# Pymodbus
from pickle import NONE
from uu import Error
from custom_components.berluf_selen_500.berluf_selen_500.modbus_impl.pymodbus import (
    serial as pymodbus_serial,
)

# Recuperator
from custom_components.berluf_selen_500.berluf_selen_500 import (
    serial as recup_serial,
)
from custom_components.berluf_selen_500.berluf_selen_500 import device as recup_device

# Persistant memory
from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave import persistant

# Functions
from custom_components.berluf_selen_500.berluf_selen_500 import funcs as recup_funcs

import asyncio
# import importlib
# importlib.reload(pymodbus_serial)
# importlib.reload(recup_serial)
# importlib.reload(recup_device)
# importlib.reload(persistant)
# importlib.reload(recup_funcs)


# %%
def connect_callb():
    print("Connected")
    return


def disconnect_callb(x: Exception | None):
    print("Disconnected")
    if x != None:
        raise x


def error_callb(ecs: list[recup_funcs.Error.Error]):
    # Save errors
    if len(ecs) == 0:
        _ec = None
    else:
        _ec = ecs[0].name
        for e in ecs[1:]:
            _ec += f", {e.name}"

    print("test")


async def main():
    # Interface for connectiong to serial
    recup_intf = recup_serial.Recup_serial_intf(
        "/dev/pts/3",
        pymodbus_serial.Pymodbus_serial_intf_builder(),
        connect_callb,
        disconnect_callb,
    )
    # Persistant memory
    persist = persistant.Persistant_dummy_factory()
    # Device's memory
    recup = recup_device.Recup_device(recup_intf, persist)

    # %%
    recup.holding_registers.get_single_val(1)

    # %%
    def bypass_callb(x: bool) -> None:
        print("test")
        return

    # %%
    bypass = recup_funcs.Bypass(recup, bypass_callb)

    # %%
    gwc = recup_funcs.GWC(recup)
    print(persist._mem)
    gwc.set(True)

    print(persist._mem)

    error = recup_funcs.Error(device=recup, callb=error_callb)

    # %%
    await recup_intf.connect()

    while True:
        # print(bypass.get())
        print(error.get())
        await asyncio.sleep(2)


asyncio.run(main())
