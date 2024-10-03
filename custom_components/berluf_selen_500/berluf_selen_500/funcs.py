from enum import Enum
from typing import List
from typing import Callable, List
from .modbus_slave.func import Device_func
from .modbus_slave.device import Device


# %%
class Supply_fan(Device_func):
    _addr: int = 70

    def __init__(self, device: Device):
        super().__init__(device)
        return

    def set(self, val: int) -> None:
        """Set supply in %"""
        self._device.holding_registers.set_single_val(self._addr, val)
        return

    def get(self) -> int:
        """Get supply in %"""
        return self._device.holding_registers.get_single_val(self._addr)


# %%
class Exhaust_fan(Device_func):
    _addr: int = 71

    def __init__(self, device: Device):
        super().__init__(device)

        return

    def set(self, val: int) -> None:
        """Set supply in %"""
        self._device.holding_registers.set_single_val(self._addr, val)
        return

    def get(self) -> int:
        """Get supply in %"""
        return self._device.holding_registers.get_single_val(self._addr)


# %%
class GWC(Device_func):
    _addr: int = 64

    def __init__(self, device: Device):
        super().__init__(device)

        return

    def set(self, val: bool) -> None:
        """Turn on or off GWC."""
        self._device.holding_registers.set_single_val(self._addr, int(val))
        return

    def get(self) -> bool:
        return bool(
            self._device.holding_registers.get_single_val(self._addr)
        )  # FIXME Check if value is invalid


# %%
class Heater_cooler(Device_func):
    class Mode(Enum):
        Cool = 0
        Heat = 1

    _addr: int = 65

    def __init__(self, device: Device):
        super().__init__(device)

        return

    def set(self, val: Mode) -> None:
        """Set heating mode"""
        self._device.holding_registers.set_single_val(self._addr, val.value)
        return

    def get(self) -> Mode:
        return Heater_cooler.Mode(
            self._device.holding_registers.get_single_val(self._addr)
        )  # FIXME Check if value is invalid


# %%
class Fan(Device_func):
    class Mode(Enum):
        Off = 0
        Max = 1
        User = 2
        Sleep = 3

    _addr: int = 72

    def __init__(self, device: Device):
        super().__init__(device)

        return

    def set(self, val: Mode) -> None:
        """Set heating mode"""
        self._device.holding_registers.set_single_val(self._addr, val.value)
        return

    def get(self) -> Mode:
        return Fan.Mode(
            self._device.holding_registers.get_single_val(self._addr)
        )  # FIXME Check if value is invalid


# %%
class Temperature_sensor(Device_func):
    _addr: int = 274

    def __init__(self, device: Device):
        super().__init__(device)

        return

    def set(self, val: int) -> None:
        """Set teperature sensor value"""
        self._device.holding_registers.set_single_val(self._addr, val)
        return

    def get(self) -> int:
        """Get teperature sensor value"""
        return self._device.holding_registers.get_single_val(self._addr)


# %%
class Error(Device_func):
    class Error(Enum):
        """All possible errors"""

        P1 = 0
        P2 = 1
        E1 = 2
        E2 = 3
        E3 = 4
        E4 = 5
        E5 = 6
        E6 = 7
        E7 = 8

    class Recup_error(Enum):
        """Bits set in registry sent by master"""

        P1 = int("00010000", 2)
        P2 = int("00100000", 2)
        E1 = int("01000000", 2)
        E7 = int("10000000", 2)

    class Visible_error(Enum):
        """Bits set by monitor
        If I checked correctly monitor can only show one option at a time
        """

        OK = int("01110000", 2)
        E1 = int("00110000", 2)
        P1 = int("01100000", 2)
        P2 = int("01010000", 2)
        P1P2 = int(
            "01000000", 2
        )  # Unused, after getting P1 or P2 error, monitor sets one of the codes above; after a while sets to this one

    # Value of temperature registers when error (E2 - E6)
    _EX = int("11111111")

    # Errors on master
    _addr_err: int = 258
    _addr_01: int = 259
    _addr_02: int = 260
    _addr_03: int = 261
    _addr_04: int = 262
    _addr_05: int = 263

    # Error visible on the screen
    _addr_vis: int = 276

    # Callbacks run when registry state changes
    def _set_change_callb_err(self, addr: int, _val: list):
        val: int = _val[0]
        pre = len(self._ecs)

        if val & Error.Recup_error.P1.value:
            self._ecs.add(Error.Error.P1)
            self._device.holding_registers.set_single_val(
                self._addr_vis, Error.Visible_error.P1.value
            )
        else:
            self._ecs.discard(Error.Error.P1)

        if val & Error.Recup_error.P2.value:
            self._ecs.add(Error.Error.P2)
            self._device.holding_registers.set_single_val(
                self._addr_vis, Error.Visible_error.P2.value
            )
        else:
            self._ecs.discard(Error.Error.P2)

        if val & Error.Recup_error.E1.value:
            self._ecs.add(Error.Error.E1)
            self._device.holding_registers.set_single_val(
                self._addr_vis, Error.Visible_error.E1.value
            )
        else:
            self._ecs.discard(Error.Error.E1)

        if val & Error.Recup_error.E7.value:
            self._ecs.add(Error.Error.E7)
        else:
            self._ecs.discard(Error.Error.E7)

        if len(self._ecs) != pre:
            self._callb(list(self._ecs))
        return

    def _set_change_callb_0X(self, val: list, ec: Error):
        if val[0] == self._EX:
            self._ecs.add(ec)
            self._callb(list(self._ecs))
        elif ec in self._ecs:
            self._ecs.discard(ec)
            self._callb(list(self._ecs))
        return

    def _set_change_callb_01(self, addr: int, val: list):
        self._set_change_callb_0X(val, Error.Error.E2)
        return

    def _set_change_callb_02(self, addr: int, val: list):
        self._set_change_callb_0X(val, Error.Error.E3)
        return

    def _set_change_callb_03(self, addr: int, val: list):
        self._set_change_callb_0X(val, Error.Error.E4)
        return

    def _set_change_callb_04(self, addr: int, val: list):
        self._set_change_callb_0X(val, Error.Error.E5)
        return

    def _set_change_callb_05(self, addr: int, val: list):
        self._set_change_callb_0X(val, Error.Error.E6)
        return

    def __init__(self, device: Device, callb: Callable[[List[Error]], None]):
        """callb is used when error arises"""
        super().__init__(device)

        self._ecs = set()
        self._callb = callb
        self._device.holding_registers.set_change_callb(
            self._addr_err, self._set_change_callb_err
        )
        self._device.holding_registers.set_change_callb(
            self._addr_01, self._set_change_callb_01
        )
        self._device.holding_registers.set_change_callb(
            self._addr_02, self._set_change_callb_02
        )
        self._device.holding_registers.set_change_callb(
            self._addr_03, self._set_change_callb_03
        )
        self._device.holding_registers.set_change_callb(
            self._addr_04, self._set_change_callb_04
        )
        self._device.holding_registers.set_change_callb(
            self._addr_05, self._set_change_callb_05
        )

        return

    def reset(self) -> list:
        """Reset errors on monitor"""
        # Reset monitor error registry so master knows we acked it
        self._device.holding_registers.set_single_val(
            self._addr_vis, Error.Visible_error.OK.value
        )

        # Refresh error list
        self._set_change_callb_err(
            self._addr_err,
            [self._device.holding_registers.get_single_val(self._addr_err)],
        )
        self._set_change_callb_01(
            self._addr_01,
            [self._device.holding_registers.get_single_val(self._addr_01)],
        )
        self._set_change_callb_02(
            self._addr_02,
            [self._device.holding_registers.get_single_val(self._addr_02)],
        )
        self._set_change_callb_03(
            self._addr_03,
            [self._device.holding_registers.get_single_val(self._addr_03)],
        )
        self._set_change_callb_04(
            self._addr_04,
            [self._device.holding_registers.get_single_val(self._addr_04)],
        )
        self._set_change_callb_05(
            self._addr_05,
            [self._device.holding_registers.get_single_val(self._addr_05)],
        )

        return list(self._ecs)

    def get(self) -> list:
        """Get all errors"""
        return list(self._ecs)


# %%
class Bypass(Device_func):
    _On = int("00001000")

    _addr: int = 258

    def _set_change_callb(self, addr: int, val: list):
        if val[0] & self._On:
            self._callb(True)
        else:
            self._callb(False)
        return

    def __init__(self, device: Device, callb: Callable[[bool], None]):
        super().__init__(device)

        self._callb = callb
        self._device.holding_registers.set_change_callb(
            self._addr, self._set_change_callb
        )

        return

    def get(self) -> bool:
        return bool(
            self._device.holding_registers.get_single_val(self._addr) & self._On
        )


# %%
class Heater(Device_func):
    _On = int("00000010")

    _addr: int = 258

    def _set_change_callb(self, addr: int, val: list):
        if val[0] & self._On:
            self._callb(True)
        else:
            self._callb(False)
        return

    def __init__(self, device: Device, callb: Callable[[bool], None]):
        super().__init__(device)

        self._callb = callb
        self._device.holding_registers.set_change_callb(
            self._addr, self._set_change_callb
        )

        return

    def get(self) -> bool:
        return bool(
            self._device.holding_registers.get_single_val(self._addr) & self._On
        )


# %%
class Pump(Device_func):
    _On = int("00000100")

    _addr: int = 258

    def _set_change_callb(self, addr: int, val: list):
        if val[0] & self._On:
            self._callb(True)
        else:
            self._callb(False)
        return

    def __init__(self, device: Device, callb: Callable[[bool], None]):
        super().__init__(device)

        self._callb = callb
        self._device.holding_registers.set_change_callb(
            self._addr, self._set_change_callb
        )

        return

    def get(self) -> bool:
        if self._device.holding_registers.get_single_val(self._addr) & self._On:
            return True
        else:
            return False


# %%
class Thermometer_01(Device_func):
    _addr: int = 259

    def _change_callb(self, addr: int, val: list):
        self._callb(val[0])

    def __init__(self, device: Device, callb: Callable[[int], None]):
        super().__init__(device)
        self._callb = callb
        self._device.holding_registers.set_change_callb(self._addr, self._change_callb)
        return

    def get(self) -> int:
        """Get thermometer value"""
        return self._device.holding_registers.get_single_val(self._addr)


# %%
class Thermometer_02(Device_func):
    _addr: int = 260

    def _change_callb(self, addr: int, val: list):
        self._callb(val[0])

    def __init__(self, device: Device, callb: Callable[[int], None]):
        super().__init__(device)
        self._callb = callb
        self._device.holding_registers.set_change_callb(self._addr, self._change_callb)
        return

    def get(self) -> int:
        """Get thermometer value"""
        return self._device.holding_registers.get_single_val(self._addr)


# %%
class Thermometer_03(Device_func):
    _addr: int = 261

    def _change_callb(self, addr: int, val: list):
        self._callb(val[0])

    def __init__(self, device: Device, callb: Callable[[int], None]):
        super().__init__(device)
        self._callb = callb
        self._device.holding_registers.set_change_callb(self._addr, self._change_callb)
        return

    def get(self) -> int:
        """Get thermometer value"""
        return self._device.holding_registers.get_single_val(self._addr)


# %%
class Thermometer_04(Device_func):
    _addr: int = 262

    def _change_callb(self, addr: int, val: list):
        self._callb(val[0])

    def __init__(self, device: Device, callb: Callable[[int], None]):
        super().__init__(device)
        self._callb = callb
        self._device.holding_registers.set_change_callb(self._addr, self._change_callb)
        return

    def get(self) -> int:
        """Get thermometer value"""
        return self._device.holding_registers.get_single_val(self._addr)


# %%
class Thermometer_05(Device_func):
    _addr: int = 263

    def _change_callb(self, addr: int, val: list):
        self._callb(val[0])

    def __init__(self, device: Device, callb: Callable[[int], None]):
        super().__init__(device)
        self._callb = callb
        self._device.holding_registers.set_change_callb(self._addr, self._change_callb)
        return

    def get(self) -> int:
        """Get thermometer value"""
        return self._device.holding_registers.get_single_val(self._addr)
