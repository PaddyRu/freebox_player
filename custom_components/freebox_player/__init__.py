from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant, ServiceCall
import logging

from .const import DOMAIN, CONF_APP_TOKEN, CONF_REMOTE_CODE
from .api import FreeboxApi

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Freebox Player integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the Freebox Player from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data
    freebox_api = FreeboxApi(hass, entry.data.get(CONF_APP_TOKEN), entry.data.get(CONF_IP_ADDRESS), entry.data.get(CONF_REMOTE_CODE))
    hass.data[DOMAIN] = freebox_api
    
    async def handle_remote(call: ServiceCall):
        """Handle the service call."""
        code = call.data.get("code")
        await freebox_api.send_command(code)

    hass.services.async_register(DOMAIN, "remote", handle_remote)
    _LOGGER.info("Freebox Player configured successfully")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a Freebox Player config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
