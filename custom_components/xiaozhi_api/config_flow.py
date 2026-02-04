"""Config flow for Xiaozhi API integration."""
from __future__ import annotations

import voluptuous as vol
import aiohttp
import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_API_URL,
    CONF_API_KEY,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    DEFAULT_API_URL,
)
from .api import XiaozhiApiClient

_LOGGER = logging.getLogger(__name__)


class XiaozhiApiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Xiaozhi API."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Check if device already configured
            await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
            self._abort_if_unique_id_configured()

            # Test connection
            session = async_get_clientsession(self.hass)
            client = XiaozhiApiClient(
                session=session,
                api_url=user_input[CONF_API_URL],
                api_key=user_input[CONF_API_KEY],
                device_id=user_input[CONF_DEVICE_ID],
            )

            try:
                if await client.test_connection():
                    return self.async_create_entry(
                        title=user_input.get(CONF_DEVICE_NAME, user_input[CONF_DEVICE_ID]),
                        data=user_input,
                    )
                else:
                    errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_URL, default=DEFAULT_API_URL): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_DEVICE_ID): str,
                    vol.Optional(CONF_DEVICE_NAME): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return XiaozhiApiOptionsFlow(config_entry)


class XiaozhiApiOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Xiaozhi API."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_URL,
                        default=self.config_entry.data.get(CONF_API_URL, DEFAULT_API_URL),
                    ): str,
                    vol.Required(
                        CONF_API_KEY,
                        default=self.config_entry.data.get(CONF_API_KEY, ""),
                    ): str,
                }
            ),
        )
