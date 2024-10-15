from .callb import (
    Callb_store,
)
from .validator import (
    Setter_validator,
    Validator,
)
from .memory import Memory_rw


# %%
class Slave_builder:
    """Base class for creating and adding slaves to the interface."""

    def create_coils(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        """Create 'coils' memory."""
        raise NotImplementedError()

    def create_discrete_inputs(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        """Create 'discrete inputs' memory."""
        raise NotImplementedError()

    def create_holding_registers(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        """Create 'holding registers' memory."""
        raise NotImplementedError()

    def create_input_registers(
        self,
        mem: dict[int, list[int]],
        validator: Validator,
        setter_validator: Setter_validator,
        callbs: Callb_store,
    ) -> None:
        """Create 'input registers' memory."""
        raise NotImplementedError()

    def create_slave(self) -> tuple[Memory_rw, Memory_rw, Memory_rw, Memory_rw]:
        """Create the slave device."""
        raise NotImplementedError()


# %%
class Device_intf:
    """Base for modbus device connectivity interface."""

    async def connect(self) -> None:
        """Connect to the interface."""
        raise NotImplementedError()

    async def disconnect(self) -> None:
        """Disconnect from the interface."""
        raise NotImplementedError()


class Device_buildable_intf(Slave_builder, Device_intf):
    """Slave_builder and Device_intf combined for convinience."""

    def __init__(self) -> None:
        return
