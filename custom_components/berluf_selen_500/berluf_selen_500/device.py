from .modbus_slave.memory import Memory_rw
from .modbus_slave.device import Device
from .modbus_slave.intf import Slave_builder
from .modbus_slave.validator import Memory_validator, Setter_validator
from .modbus_slave.callb import Callb_store
from copy import deepcopy

from custom_components.berluf_selen_500.berluf_selen_500.modbus_slave import callb


# %%
class Recup_device(Device):
    def __init__(
        self,
        impl_builder: Slave_builder,
        persistant: dict[int, list[int]] | None = None,
    ):
        self._create_device(impl_builder, persistant)
        return

    def _get_valid_mem(
        self,
        reg_mem: dict[int, list[int]],
    ) -> list:
        # Set valid addresses and persistant
        valid_mem = []
        for a, v in reg_mem.items():  # TODO move to try: except:
            len_ = len(v)
            # Validator
            valid_mem.extend(range(a, a + len_))

        return valid_mem

    def _create_device(
        self,
        impl_builder: Slave_builder,
        persistant: dict[int, list[int]] | None = None,
    ):
        self._create_holding_registers(
            impl_builder,
            persistant,
        )
        (
            self.coils,
            self.discrete_inputs,
            self.holding_registers,
            self.input_registers,
        ) = impl_builder.create_slave()

        return

    def _create_holding_registers(
        self,
        impl_builder: Slave_builder,
        persistant: dict[int, list[int]] | None = None,
    ) -> None:
        callbs = Callb_store()

        # Default memory
        mem_slave = {
            0: [1, 0, 25, 18, 18, 26, 22, 5, 60, 60, 30],
            60: [2, 25, 0, 24, 1, 0, 25, 25, 25, 0, 10, 10, 2],
            274: [26, 3, 112, 0, 16],
        }
        mem_master = {258: [0, 20, 20, 20, 20, 20]}

        # All addresses
        addrs = self._get_valid_mem(deepcopy(mem_slave))
        setter_validator = Setter_validator(deepcopy(addrs))
        addrs.extend(self._get_valid_mem(mem_master))
        validator = Memory_validator(addrs)

        # Concatenate memory
        mem = mem_slave
        mem.update(mem_master)

        if persistant is not None:
            # Use loaded memory, but first check if layout matches
            for (a_1, v_1), (a_2, v_2) in zip(
                sorted(mem.items()), sorted(persistant.items())
            ):
                if a_1 != a_2:
                    raise RuntimeError(f"Addresses do not match: {a_2} is not {a_1}.")
                elif len(v_1) != len(v_2):
                    raise RuntimeError(
                        f"Addresse's value len do not match: {v_2} is not {v_1} for address {a_1}."
                    )

            mem = persistant

        impl_builder.create_holding_registers(mem, validator, setter_validator, callbs)
        return
