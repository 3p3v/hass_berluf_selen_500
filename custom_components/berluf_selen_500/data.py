"""Custom types for berluf_selen_500"""

from __future__ import annotations
import importlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

# Underlying recuperator implementation
from .berluf_selen_500.modbus_slave.intf import Device_intf
from .berluf_selen_500.device import Recup_device
# from .berluf_selen_500.funcs import Recup_timeout_manager

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration


type Berluf_selen_500_ConfigEntry = ConfigEntry[Berluf_selen_500_Data]


# @dataclass
class Berluf_selen_500_Data:
    """Data for the Berluf Selen 500 integration"""

    def __init__(self, intf: Device_intf, device: Recup_device) -> None:
        # Interface used for connecting/disconnecting
        self._intf = intf
        # Slave memory
        self._device = device
        # Timer that needs to be disabled while deleting integration
        self._timer = None
        return

    def get_intf(self) -> Device_intf:
        return self._intf

    def get_device(self) -> Recup_device:
        return self._device

    def set_timer(self, timer) -> None:
        if self._timer is None:
            self._timer = timer
        else:
            raise RuntimeError("Timer has already been set.")

    def get_timer(self):
        if self._timer is not None:
            return self._timer
        else:
            raise RuntimeError("Timer hasn't been set yet.")
