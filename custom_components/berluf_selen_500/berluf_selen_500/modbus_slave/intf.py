from typing import Tuple

from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.callb import (
    Callb_store,
)
from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave.validator import (
    Setter_validator,
    Validator,
)
from .memory import Memory_rw


# %%
class Slave_builder:
    """Base class for creating and adding slaves to the interface"""

    # TODO create method to generate memory
    # TODO create method 'attach' to attach device to intf

    def create_coils(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        raise NotImplementedError()

    def create_discrete_inputs(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        raise NotImplementedError()

    def create_holding_registers(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        raise NotImplementedError()

    def create_input_registers(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        raise NotImplementedError()

    def create_slave(self) -> tuple[Memory_rw, Memory_rw, Memory_rw, Memory_rw]:
        raise NotImplementedError()


# %%
class Device_intf:
    """Base for modbus device connectivity interface"""

    async def connect(self) -> None:
        raise NotImplementedError()

    async def disconnect(self) -> None:
        raise NotImplementedError()


class Device_buildable_intf(Slave_builder, Device_intf):
    def __init__(self):
        return
