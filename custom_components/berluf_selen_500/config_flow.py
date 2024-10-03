"""Config flow for berluf_selen_500."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_PORT
from homeassistant.helpers import selector

from .defs import LOGGER, DOMAIN


class Berluf_selen_500_FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            com = user_input[CONF_PORT]

            # TODO let use choose TCP
            # TODO Test if port exists

            return self.async_create_entry(
                title=user_input[CONF_PORT],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )
