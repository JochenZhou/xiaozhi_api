"""Select platform for Xiaozhi API."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME, PLAYER_MODES, THEMES

SELECT_DESCRIPTIONS = [
    SelectEntityDescription(
        key="player_mode",
        translation_key="player_mode",
        icon="mdi:playlist-play",
        options=list(PLAYER_MODES.keys()),
    ),
    SelectEntityDescription(
        key="theme",
        translation_key="theme",
        icon="mdi:theme-light-dark",
        options=list(THEMES.keys()),
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Xiaozhi selects."""
    data = hass.data[DOMAIN][entry.entry_id]
    client = data["client"]
    device_id = entry.data[CONF_DEVICE_ID]
    device_name = entry.data.get(CONF_DEVICE_NAME, device_id)

    entities = [
        XiaozhiSelect(client, device_id, device_name, description)
        for description in SELECT_DESCRIPTIONS
    ]
    async_add_entities(entities)


class XiaozhiSelect(SelectEntity):
    """Xiaozhi select entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        client,
        device_id: str,
        device_name: str,
        description: SelectEntityDescription,
    ) -> None:
        """Initialize the select."""
        self._client = client
        self._device_id = device_id
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_current_option = description.options[0] if description.options else None
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="Xiaozhi",
            model="Smart Device",
        )

    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        key = self.entity_description.key
        if key == "player_mode":
            mode = PLAYER_MODES.get(option, option)
            await self._client.set_player_mode(mode)
        elif key == "theme":
            theme = THEMES.get(option, option)
            await self._client.set_theme(theme)
        self._attr_current_option = option
        self.async_write_ha_state()
