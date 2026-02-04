"""Number platform for Xiaozhi API."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME

NUMBER_DESCRIPTIONS = [
    NumberEntityDescription(
        key="volume",
        translation_key="volume",
        icon="mdi:volume-high",
        native_min_value=0,
        native_max_value=100,
        native_step=1,
    ),
    NumberEntityDescription(
        key="brightness",
        translation_key="brightness",
        icon="mdi:brightness-6",
        native_min_value=0,
        native_max_value=100,
        native_step=1,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Xiaozhi numbers."""
    data = hass.data[DOMAIN][entry.entry_id]
    client = data["client"]
    device_id = entry.data[CONF_DEVICE_ID]
    device_name = entry.data.get(CONF_DEVICE_NAME, device_id)

    entities = [
        XiaozhiNumber(client, device_id, device_name, description)
        for description in NUMBER_DESCRIPTIONS
    ]
    async_add_entities(entities)


class XiaozhiNumber(NumberEntity):
    """Xiaozhi number entity."""

    _attr_has_entity_name = True
    _attr_mode = NumberMode.SLIDER

    def __init__(
        self,
        client,
        device_id: str,
        device_name: str,
        description: NumberEntityDescription,
    ) -> None:
        """Initialize the number."""
        self._client = client
        self._device_id = device_id
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_native_value = 50
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="Xiaozhi",
            model="Smart Device",
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        int_value = int(value)
        key = self.entity_description.key
        if key == "volume":
            await self._client.set_volume(int_value)
        elif key == "brightness":
            await self._client.set_brightness(int_value)
        self._attr_native_value = int_value
        self.async_write_ha_state()
