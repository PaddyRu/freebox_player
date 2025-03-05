from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS
import asyncio
import aiohttp
import voluptuous as vol
import logging

from .const import (
    DOMAIN, BASE_URL, AUTH_URL,
    CONF_REMOTE_CODE, CONF_APP_TOKEN,
    CONF_APP_ID, CONF_APP_NAME, CONF_APP_VERSION, CONF_DEVICE_NAME,
    APP_ID, APP_NAME, APP_VERSION, DEVICE_NAME
)

class FreeboxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Freebox Player."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            self.host = user_input[CONF_IP_ADDRESS]
            self.remote_code = user_input[CONF_REMOTE_CODE]
            return await self.async_step_link()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_IP_ADDRESS): str, vol.Required(CONF_REMOTE_CODE): str}),
            description_placeholders={}
        )

    async def async_step_link(self, user_input=None):
        """Handle authentication process."""
        session = aiohttp.ClientSession()
        try:
            async with session.post(f"{BASE_URL}{AUTH_URL}", json={
                CONF_APP_ID: APP_ID,
                CONF_APP_NAME: APP_NAME,
                CONF_APP_VERSION: APP_VERSION,
                CONF_DEVICE_NAME: DEVICE_NAME,
            }) as response:
                data = await response.json()
                if "result" in data:
                    track_id = data["result"].get("track_id")
                    app_token = data["result"].get("app_token")
                    if track_id and app_token:
                        return await self._poll_authorization(session, track_id, app_token)
                _LOGGER.error("Erreur lors de la récupération du track_id: %s", data)
        except Exception as err:
            _LOGGER.error("Exception lors de la communication avec la Freebox: %s", err)
            return self.async_show_form(
                step_id="user", errors={"base": "cannot_connect"}
            )
        finally:
            await session.close()
        
        return self.async_show_form(
            step_id="user", errors={"base": "unknown"}
        )

    async def _poll_authorization(self, session, track_id, app_token):
        """Poll the Freebox to check authorization status."""
        url = f"{BASE_URL}{AUTH_URL}{track_id}"
        for _ in range(30):  # Poll for up to 30 seconds
            try:
                async with session.get(url) as response:
                    data = await response.json()
                    if "result" in data:
                        status = data["result"].get("status")
                        if status == "granted":
                            return self.async_create_entry(title="Freebox Player", data = {
                                CONF_APP_TOKEN: app_token,
                                CONF_IP_ADDRESS: self.host,
                                CONF_REMOTE_CODE: self.remote_code}
                            )
                        elif status in ["denied", "timeout"]:
                            return self.async_show_form(
                                step_id="user", errors={"base": "auth_failed"}
                            )
            except Exception as err:
                _LOGGER.error("Erreur lors du polling de l'autorisation: %s", err)
                return self.async_show_form(
                    step_id="user", errors={"base": "cannot_connect"}
                )
            await asyncio.sleep(2)  # Wait 2 seconds before retrying
        
        return self.async_show_form(
            step_id="user", errors={"base": "timeout"}
        )
