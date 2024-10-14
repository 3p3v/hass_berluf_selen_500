"""Definitions for berluf_selen_500"""

from logging import Logger, getLogger

from .data import Berluf_selen_500_ConfigEntry

LOGGER: Logger = getLogger(__package__)

DOMAIN = "berluf_selen_500"

# Store definitions
LAST_SET = "last_set"
USER_MODE = "usr_mode"


def get_default_store_name(entry: Berluf_selen_500_ConfigEntry):
    return entry.entry_id + LAST_SET
