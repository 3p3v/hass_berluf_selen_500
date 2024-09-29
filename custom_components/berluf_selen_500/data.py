""" Custom types for berluf_selen_500 """

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    # Underlying recuperator implementation
    from .recup.device import Recup_device


type Berluf_selen_500_ConfigEntry = ConfigEntry[Berluf_selen_500_Data]


@dataclass
class Berluf_selen_500_Data:
    """ Data for the Berluf Selen 500 integration """

    # Named recuperator devices managed by the integraion
    # _devices: List[Recup_device] # TODO Change to dict?
    _device: Recup_device
    
    def get_device(self) -> Recup_device:
        return self._device
        # if (len(self._devices)):
        #     return self._devices[-1]
        # else: 
        #     raise RuntimeError("No recuperator devices added yet")