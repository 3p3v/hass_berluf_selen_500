"""Berluf Selen 500 integration."""

from __future__ import annotations
from typing import TYPE_CHECKING
import importlib

from homeassistant.const import CONF_PORT, Platform

# from homeassistant.loader import async_get_loaded_integration
from homeassistant.exceptions import HomeAssistantError

from .defs import LOGGER

from .data import Berluf_selen_500_Data
from .data import Berluf_selen_500_ConfigEntry
from .defs import HOME_PATH

from .berluf_selen_500.device import Recup_device
from .berluf_selen_500.serial import Recup_serial_intf
from .berluf_selen_500.serial import Recup_serial_intf
from .berluf_selen_500.modbus_slave.persistant import Persistant_dummy
from .berluf_selen_500.modbus_impl.pymodbus.serial import Pymodbus_serial_intf_builder


if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.SENSOR,
    # Platform.FAN,
    Platform.NUMBER,
    Platform.SELECT,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: Berluf_selen_500_ConfigEntry,
) -> bool:
    """Set up this integration using UI."""

    def connect_callb() -> None:
        return

    def disconnect_callb(ec: Exception | None) -> None:
        # if ec is not None:
        # raise HomeAssistantError()
        return

    # Interface for connecting to serial
    intf = Recup_serial_intf(
        entry.data[CONF_PORT],
        Pymodbus_serial_intf_builder(),
        connect_callb,
        disconnect_callb,
    )
    # Persistant memory
    persist = Persistant_dummy("holding_registers")
    # Device
    device = Recup_device(intf, persist)

    entry.runtime_data = Berluf_selen_500_Data(intf=intf, device=device)

    # Connect to interface
    try:
        LOGGER.debug("Connecting to specyfied interface...")
        await intf.connect()
        LOGGER.debug("Connected successfully.")

        LOGGER.debug(
            f"TEST: {entry.runtime_data.get_device().holding_registers.get_single_val(1)}"
        )
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        entry.async_on_unload(entry.add_update_listener(async_reload_entry))

        LOGGER.debug("Config successfull.")
        return True
    except Exception as e:
        LOGGER.error(f"Error occured during setup: {e}")
        raise e


async def async_unload_entry(
    hass: HomeAssistant,
    entry: Berluf_selen_500_ConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    await entry.runtime_data.get_intf().disconnect()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: Berluf_selen_500_ConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
    return
