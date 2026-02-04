"""Text platform for Xiaozhi API."""
from __future__ import annotations

from homeassistant.components.text import TextEntity, TextEntityDescription, TextMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME

TEXT_DESCRIPTIONS = [
    TextEntityDescription(
        key="chat_message",
        translation_key="chat_message",
        icon="mdi:message-text",
    ),
    TextEntityDescription(
        key="play_music",
        translation_key="play_music",
        icon="mdi:music-box-outline",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Xiaozhi text entities."""
    data = hass.data[DOMAIN][entry.entry_id]
    client = data["client"]
    device_id = entry.data[CONF_DEVICE_ID]
    device_name = entry.data.get(CONF_DEVICE_NAME, device_id)

    entities = [
        XiaozhiText(client, device_id, device_name, description)
        for description in TEXT_DESCRIPTIONS
    ]
    async_add_entities(entities)


class XiaozhiText(TextEntity):
    """Xiaozhi text entity."""

    _attr_has_entity_name = True
    _attr_mode = TextMode.TEXT
    _attr_native_max = 500

    def __init__(
        self,
        client,
        device_id: str,
        device_name: str,
        description: TextEntityDescription,
    ) -> None:
        """Initialize the text entity."""
        self._client = client
        self._device_id = device_id
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_native_value = ""
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="Xiaozhi",
            model="Smart Device",
        )

    async def async_set_value(self, value: str) -> None:
        """Set the value and send to device."""
        key = self.entity_description.key
        if key == "chat_message":
            await self._client.send_chat_message(value)
        elif key == "play_music":
            await self._client.play_music(value)
        self._attr_native_value = value
        self.async_write_ha_state()
