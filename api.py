"""API client for Xiaozhi devices."""
from __future__ import annotations

import aiohttp
import logging
from typing import Any

from .const import (
    API_SEND_CHAT,
    API_SEND_IDLE,
    API_PLAY_MUSIC,
    API_STOP_MUSIC,
    API_RESUME_MUSIC,
    API_NEXT_MUSIC,
    API_PREV_MUSIC,
    API_PLAYER_MODE,
    API_VOLUME,
    API_BRIGHTNESS,
    API_THEME,
)

_LOGGER = logging.getLogger(__name__)


class XiaozhiApiClient:
    """API client for Xiaozhi devices."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        api_url: str,
        api_key: str,
        device_id: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._api_url = api_url.rstrip("/")
        self._api_key = api_key
        self._device_id = device_id

    def _get_headers(self) -> dict[str, str]:
        """Get request headers."""
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def _request(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Make API request."""
        url = f"{self._api_url}{endpoint}"
        try:
            async with self._session.post(
                url, json=data, headers=self._get_headers()
            ) as response:
                result = await response.json()
                if result.get("code") != 200:
                    _LOGGER.error(
                        "API request failed: %s - %s",
                        result.get("code"),
                        result.get("message"),
                    )
                return result
        except aiohttp.ClientError as err:
            _LOGGER.error("API request error: %s", err)
            return {"code": -1, "message": str(err)}

    async def test_connection(self) -> bool:
        """Test API connection."""
        result = await self.send_idle()
        return result.get("code") == 200

    async def send_chat_message(self, message: str) -> dict[str, Any]:
        """Send chat message to device."""
        return await self._request(
            API_SEND_CHAT,
            {"deviceId": self._device_id, "message": message},
        )

    async def send_idle(self) -> dict[str, Any]:
        """Send idle command to device."""
        return await self._request(
            API_SEND_IDLE,
            {"deviceId": self._device_id},
        )

    async def play_music(self, keywords: str) -> dict[str, Any]:
        """Play music by keywords."""
        return await self._request(
            API_PLAY_MUSIC,
            {"deviceId": self._device_id, "keywords": keywords},
        )

    async def stop_music(self) -> dict[str, Any]:
        """Stop music playback."""
        return await self._request(
            API_STOP_MUSIC,
            {"deviceId": self._device_id},
        )

    async def resume_music(self) -> dict[str, Any]:
        """Resume music playback."""
        return await self._request(
            API_RESUME_MUSIC,
            {"deviceId": self._device_id},
        )

    async def next_track(self) -> dict[str, Any]:
        """Play next track."""
        return await self._request(
            API_NEXT_MUSIC,
            {"deviceId": self._device_id},
        )

    async def previous_track(self) -> dict[str, Any]:
        """Play previous track."""
        return await self._request(
            API_PREV_MUSIC,
            {"deviceId": self._device_id},
        )

    async def set_player_mode(self, mode: str) -> dict[str, Any]:
        """Set player mode."""
        return await self._request(
            API_PLAYER_MODE,
            {"deviceId": self._device_id, "playerMode": mode},
        )

    async def set_volume(self, volume: int) -> dict[str, Any]:
        """Set volume (0-100)."""
        return await self._request(
            API_VOLUME,
            {"deviceId": self._device_id, "value": volume},
        )

    async def set_brightness(self, brightness: int) -> dict[str, Any]:
        """Set brightness (0-100)."""
        return await self._request(
            API_BRIGHTNESS,
            {"deviceId": self._device_id, "value": brightness},
        )

    async def set_theme(self, theme: str) -> dict[str, Any]:
        """Set theme (light/dark)."""
        return await self._request(
            API_THEME,
            {"deviceId": self._device_id, "value": theme},
        )
