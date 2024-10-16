# %%
# !pip3 install pyserial
# !pip3 install pymodbus
# !pip3 install homeassistant


# %%
# Pymodbus
from custom_components.berluf_selen_500.berluf_selen_500.modbus_impl.asyncio.timer import (
    Asyncio_timer_factory,
)
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
        "/dev/pts/4",
        pymodbus_serial.Pymodbus_serial_intf_builder(),
        connect_callb,
        disconnect_callb,
    )
    # Persistant memory
    # persist = persistant.Persistant_dummy("holding_registers")
    # Device's memory
    recup = recup_device.Recup_device(recup_intf, None)

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
    # print(persist._mem)
    gwc.set(False)

    # print(persist._mem)

    error = recup_funcs.Error(
        device=recup, timer_factory=Asyncio_timer_factory(), callb=error_callb
    )

    fan_initializer = recup_funcs.Fans_initializer(recup)
    supply_fan = recup_funcs.Supply_fan(fan_initializer)

    # %%
    await recup_intf.connect()

    while True:
        # print(bypass.get())
        print(error.get())
        print(supply_fan.set(2))
        await asyncio.sleep(2)


asyncio.run(main())
