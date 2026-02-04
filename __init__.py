"""The Xiaozhi API integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_API_URL,
    CONF_API_KEY,
    CONF_DEVICE_ID,
    PLAYER_MODES,
)
from .api import XiaozhiApiClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.TEXT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Xiaozhi API from a config entry."""
    session = async_get_clientsession(hass)

    client = XiaozhiApiClient(
        session=session,
        api_url=entry.data[CONF_API_URL],
        api_key=entry.data[CONF_API_KEY],
        device_id=entry.data[CONF_DEVICE_ID],
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "device_id": entry.data[CONF_DEVICE_ID],
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    await _async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def _async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Xiaozhi API."""

    async def _get_client(call: ServiceCall) -> XiaozhiApiClient | None:
        """Get client from service call."""
        device_id = call.data.get("device_id")
        for entry_data in hass.data[DOMAIN].values():
            if entry_data["device_id"] == device_id:
                return entry_data["client"]
        _LOGGER.error("Device not found: %s", device_id)
        return None

    async def send_chat_message(call: ServiceCall) -> None:
        """Send chat message service."""
        client = await _get_client(call)
        if client:
            await client.send_chat_message(call.data["message"])

    async def play_music(call: ServiceCall) -> None:
        """Play music service."""
        client = await _get_client(call)
        if client:
            await client.play_music(call.data["keywords"])

    async def set_volume(call: ServiceCall) -> None:
        """Set volume service."""
        client = await _get_client(call)
        if client:
            await client.set_volume(call.data["volume"])

    async def set_brightness(call: ServiceCall) -> None:
        """Set brightness service."""
        client = await _get_client(call)
        if client:
            await client.set_brightness(call.data["brightness"])

    async def set_player_mode(call: ServiceCall) -> None:
        """Set player mode service."""
        client = await _get_client(call)
        if client:
            mode = PLAYER_MODES.get(call.data["mode"], call.data["mode"])
            await client.set_player_mode(mode)

    async def set_theme(call: ServiceCall) -> None:
        """Set theme service."""
        client = await _get_client(call)
        if client:
            await client.set_theme(call.data["theme"])

    if not hass.services.has_service(DOMAIN, "send_chat_message"):
        hass.services.async_register(DOMAIN, "send_chat_message", send_chat_message)
        hass.services.async_register(DOMAIN, "play_music", play_music)
        hass.services.async_register(DOMAIN, "set_volume", set_volume)
        hass.services.async_register(DOMAIN, "set_brightness", set_brightness)
        hass.services.async_register(DOMAIN, "set_player_mode", set_player_mode)
        hass.services.async_register(DOMAIN, "set_theme", set_theme)
