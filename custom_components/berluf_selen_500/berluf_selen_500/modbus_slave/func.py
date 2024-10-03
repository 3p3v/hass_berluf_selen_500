from .device import Device


# %%
class Device_func:
    """Base class for some functionality of a device"""

    def __init__(self, device: Device):
        self._device: Device = device
