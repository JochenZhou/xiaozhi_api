"""Constants for Xiaozhi API integration."""

DOMAIN = "xiaozhi_api"

CONF_API_URL = "api_url"
CONF_API_KEY = "api_key"
CONF_DEVICE_ID = "device_id"
CONF_DEVICE_NAME = "device_name"

DEFAULT_API_URL = "http://101.35.234.159/Xiaozhi"

# API Endpoints
API_SEND_CHAT = "/api/xiaozhi/SendChatMessage"
API_SEND_IDLE = "/api/xiaozhi/SendIdleMessage"
API_PLAY_MUSIC = "/api/xiaozhi/SendPlayMusicMessage"
API_STOP_MUSIC = "/api/xiaozhi/SendStopMusicMessage"
API_RESUME_MUSIC = "/api/xiaozhi/SendResumeMusicMessage"
API_NEXT_MUSIC = "/api/xiaozhi/SendPlayNextMusicMessage"
API_PREV_MUSIC = "/api/xiaozhi/SendPlayPrevMusicMessage"
API_PLAYER_MODE = "/api/xiaozhi/SendPlayerModeMessage"
API_VOLUME = "/api/xiaozhi/SendVolumeMessage"
API_BRIGHTNESS = "/api/xiaozhi/SendBrightnessMessage"
API_THEME = "/api/xiaozhi/SendThemeMessage"

# Player modes
PLAYER_MODES = {
    "sequence": "SEQUENCE",
    "random": "RANDOM",
    "list_loop": "LIST_LOOP",
    "single_loop": "SINGLE_LOOP",
}

PLAYER_MODE_NAMES = {
    "sequence": "顺序播放",
    "random": "随机播放",
    "list_loop": "列表循环",
    "single_loop": "单曲循环",
}

# Theme options
THEMES = {
    "light": "light",
    "dark": "dark",
}

THEME_NAMES = {
    "light": "浅色主题",
    "dark": "深色主题",
}
