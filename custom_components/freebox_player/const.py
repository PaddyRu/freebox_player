import logging

DOMAIN = "freebox_player_api"

LOGGER = logging.getLogger("custom_components." + DOMAIN)

BASE_URL = "http://mafreebox.freebox.fr/api/v13"
AUTH_URL = "/login/authorize/"
CHALLENGE_URL = "/login/"
SESSION_URL = "/login/session/"
PLAYER_URL = "/player/"
CONTROL_URL = "/api/v14/control/"

CONF_REMOTE_CODE = "remote_code"
CONF_APP_ID = "app_id"
CONF_APP_NAME = "app_name"
CONF_APP_VERSION = "app_version"
CONF_DEVICE_NAME = "device_name"

APP_ID = DOMAIN
APP_NAME = "Freebox Player"
APP_VERSION = "1.0"
DEVICE_NAME = "Home Assistant"

CONF_APP_TOKEN = "app_token"
CONF_SESSION_TOKEN = "session_token"

ERROR_AUTH_FAILED = "Échec de l'authentification"
ERROR_UNKNOWN_STATE = "État inconnu"
