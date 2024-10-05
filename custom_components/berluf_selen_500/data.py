"""Custom types for berluf_selen_500"""

from __future__ import annotations
import importlib
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import List

from .defs import HOME_PATH

# Underlying recuperator implementation
from .berluf_selen_500.modbus_slave.intf import Device_intf
from .berluf_selen_500.device import Recup_device
from .berluf_selen_500.funcs import Recup_timeout_manager

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration


type Berluf_selen_500_ConfigEntry = ConfigEntry[Berluf_selen_500_Data]


# @dataclass
class Berluf_selen_500_Data:
    """Data for the Berluf Selen 500 integration"""

    def __init__(
        self, intf: Device_intf, device: Recup_device, timer=Recup_timeout_manager
    ):
        self._intf = intf
        self._device = device
        self._timer = timer

        # _intf#: Device_intf
        # # Named recuperator devices managed by the integraion
        # # _devices: List[Recup_device] # TODO Change to dict?
        # _device: Recup_device
        return

    def get_intf(self) -> Device_intf:
        return self._intf

    def get_device(self) -> Recup_device:
        return self._device
        # if (len(self._devices)):
        #     return self._devices[-1]
        # else:
        #     raise RuntimeError("No recuperator devices added yet")
