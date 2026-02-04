"""Button platform for Xiaozhi API."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME

BUTTON_DESCRIPTIONS = [
    ButtonEntityDescription(
        key="idle",
        translation_key="idle",
        icon="mdi:sleep",
    ),
    ButtonEntityDescription(
        key="stop_music",
        translation_key="stop_music",
        icon="mdi:stop",
    ),
    ButtonEntityDescription(
        key="resume_music",
        translation_key="resume_music",
        icon="mdi:play",
    ),
    ButtonEntityDescription(
        key="next_track",
        translation_key="next_track",
        icon="mdi:skip-next",
    ),
    ButtonEntityDescription(
        key="previous_track",
        translation_key="previous_track",
        icon="mdi:skip-previous",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Xiaozhi buttons."""
    data = hass.data[DOMAIN][entry.entry_id]
    client = data["client"]
    device_id = entry.data[CONF_DEVICE_ID]
    device_name = entry.data.get(CONF_DEVICE_NAME, device_id)

    entities = [
        XiaozhiButton(client, device_id, device_name, description)
        for description in BUTTON_DESCRIPTIONS
    ]
    async_add_entities(entities)


class XiaozhiButton(ButtonEntity):
    """Xiaozhi button entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        client,
        device_id: str,
        device_name: str,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        self._client = client
        self._device_id = device_id
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="Xiaozhi",
            model="Smart Device",
        )

    async def async_press(self) -> None:
        """Handle button press."""
        key = self.entity_description.key
        if key == "idle":
            await self._client.send_idle()
        elif key == "stop_music":
            await self._client.stop_music()
        elif key == "resume_music":
            await self._client.resume_music()
        elif key == "next_track":
            await self._client.next_track()
        elif key == "previous_track":
            await self._client.previous_track()
