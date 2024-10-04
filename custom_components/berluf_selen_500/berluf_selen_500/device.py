from .modbus_slave.memory import Memory_rw, Memory_rw_initializer
from .modbus_slave.device import Device
from .modbus_slave.intf import Slave_builder
from .modbus_slave.persistant import Memory_persistant, Memory_persistant_factory
from .modbus_slave.validator import (
    Memory_validator,
    Equal_handler,
    One_of_handler,
    Many_handler,
    Smaller_equal_handler,
    Bigger_equal_handler,
)
from .modbus_slave.callb import Callb_store


# %%
class Recup_device(Device):
    def __init__(
        self, impl_builder: Slave_builder, persistant_factory: Memory_persistant_factory
    ):
        # self._impl_builder: Impl_builder = impl_builder
        self._persistant_factory: Memory_persistant_factory = persistant_factory

        self._create_device(*impl_builder.create_slave())
        return

    def _get_valid_mem(
        self, reg_mem: dict, callbs: Callb_store, persistant: Memory_persistant
    ) -> list:
        # Set valid addresses and persistant
        valid_mem = []
        for a, v in reg_mem.items():  # TODO move to try: except:
            len_ = len(v)
            # Validator
            valid_mem.extend(range(a, a + len_))
            # Persistant
            callbs.add_callb(a, lambda addr, vals: persistant.save(addr, vals), len_)

        return valid_mem

    def _create_memory(
        self,
        mem: Memory_rw_initializer,
        reg_mem_r: dict,
        reg_mem_rw: dict,
        persistant: Memory_persistant,
    ) -> (
        Memory_rw
    ):  # TODO accept only Memory_rw or return configured validator and persistant
        try:
            reg_mem = persistant.load()
        except:
            # Set runtime memory
            reg_mem = {}
            reg_mem.update(reg_mem_r)
            reg_mem.update(reg_mem_rw)

            # Save default values to persistant
            for a, v in reg_mem.items():
                persistant.save(a, v)

        # Set memory
        mem.set_memory(reg_mem)

        callbs = Callb_store()

        # Get valid addresses and persistant for registers writable by device itself
        valid_mem_r = self._get_valid_mem(reg_mem_r, callbs, persistant)

        # Get valid addresses and persistant for registers writable by master
        valid_mem_rw = self._get_valid_mem(reg_mem_rw, callbs, persistant)
        valid_mem_rw.extend(valid_mem_r)

        # Set valid addresses
        mem.set_callb_service(callbs)
        mem.set_validator_service(
            Memory_validator(valid_mem_r), Memory_validator(valid_mem_rw)
        )
        return mem

    def _create_device(
        self, coils, discrete_inputs, holding_registers, input_registers
    ):
        holding_registers_persistant = self._persistant_factory.create_persistant(
            "holding_registers"
        )
        holding_registers_mem_r = {
            0: [1, 0, 25, 18, 18, 26, 22, 5, 60, 60, 30],
            60: [2, 25, 0, 24, 1, 0, 25, 25, 25, 0, 10, 10, 2],
            274: [26, 3, 112, 0, 16],
        }
        holding_registers_mem_r_v = {
            0: [
                Equal_handler(1),
                Equal_handler(0),
                Equal_handler(25),
                Equal_handler(18),
                Equal_handler(18),
                Equal_handler(26),
                Equal_handler(22),
                Equal_handler(5),
                Equal_handler(60),
                Equal_handler(60),
                Equal_handler(30),
            ],
            60: [
                Equal_handler(2),
                Equal_handler(25),
                Equal_handler(0),
                Equal_handler(24),
                One_of_handler([0, 1]),
                One_of_handler([0, 1]),
                Equal_handler(25),
                Equal_handler(25),
                Equal_handler(25),
                One_of_handler([0, 1, 2]),
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(100)]),
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(100)]),
                One_of_handler([0, 1, 2, 3]),
            ],
            274: [
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(50)]),
                One_of_handler([3, 5, 7, 8]),
                Many_handler(
                    [Bigger_equal_handler(0), Smaller_equal_handler(int("11111111", 2))]
                ),
                One_of_handler([0, 1]),
                Equal_handler(16),
            ],
        }
        holding_registers_mem_rw = {258: [0, 20, 20, 20, 20, 20]}
        holding_registers_mem_rw_v = {
            258: [
                Many_handler(
                    [Bigger_equal_handler(0), Smaller_equal_handler(int("11111111", 2))]
                ),
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(100)]),
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(100)]),
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(100)]),
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(100)]),
                Many_handler([Bigger_equal_handler(0), Smaller_equal_handler(100)]),
            ],
        }
        self.holding_registers = self._create_memory(
            holding_registers,
            holding_registers_mem_r,
            holding_registers_mem_rw,
            holding_registers_persistant,
        )
        self.coils = None
        self.discrete_inputs = None
        self.input_registers = None

        return
