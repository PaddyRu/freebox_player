import logging
import aiohttp
import asyncio
import hashlib
import hmac
import json

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, APP_ID, BASE_URL, CHALLENGE_URL, SESSION_URL, PLAYER_URL, CONTROL_URL

_LOGGER = logging.getLogger(__name__)

class FreeboxApi:
    def __init__(self, hass: HomeAssistant, app_token: str, host: str, remote_code: str):
        self.hass = hass
        self.app_token = app_token
        self.host = host
        self.remote_code = remote_code
        self.session_token = None
        self.session = async_get_clientsession(hass)

    async def get_challenge(self):
        """Retrieve challenge from Freebox for authentication."""
        url = f"{BASE_URL}{CHALLENGE_URL}"
        async with self.session.get(url) as response:
            data = await response.json()
            return data["result"]["challenge"] if "result" in data else None

    async def authenticate(self):
        """Perform authentication and retrieve session token."""
        challenge = await self.get_challenge()
        if not challenge:
            _LOGGER.error("Failed to get challenge from Freebox.")
            return False
        
        password = hmac.new(self.app_token.encode(), challenge.encode(), hashlib.sha1).hexdigest()
        
        payload = {"app_id": APP_ID, "password": password}
        url = f"{BASE_URL}{SESSION_URL}"
        async with self.session.post(url, json=payload) as response:
            data = await response.json()
            if "result" in data and data["success"]:
                self.session_token = data["result"]["session_token"]
                return True
            else:
                _LOGGER.error("Authentication failed: %s", data)
                return False

    async def get_player_id(self):
        """Retrieve the Freebox Player ID."""
        url = f"{BASE_URL}{PLAYER_URL}"
        headers = {"X-Fbx-App-Auth": self.session_token}

        async with self.session.get(url, headers=headers) as response:
            data = await response.json()
            if response.status == 200 and data.get("success"):
                players = data.get("result", [])
                if players:
                    return players[0]["id"]  # Use the first available player
            elif response.status in (401, 403):  # Token expired, retry authentication
                    _LOGGER.warning("Session token expired, renewing...")
                    if await self.authenticate():
                        return await self.get_player_id()
            _LOGGER.error("Failed to retrieve Freebox Player ID")
            return None

    async def send_command(self, command: str):
        """Send a command to the Freebox Player."""
        if not self.session_token:
            success = await self.authenticate()
            if not success:
                _LOGGER.error("Could not authenticate with Freebox.")
                return False
        
        player_id = await self.get_player_id()
        if not player_id:
            return False

        url = f"{BASE_URL}{PLAYER_URL}{player_id}{CONTROL_URL}"
        headers = {"X-Fbx-App-Auth": self.session_token}
        func = None
        if command in ("play_pause", "stop", "prev", "next"):
            url = f"{url}mediactrl"
            payload = {"cmd": command}
            func = self.session.post
        elif command in ("mute","unmute"):
            url = f"{url}volume"
            payload = {"mute": "unmute" not in command}
            func = self.session.put
        elif "https://" in command or "vodservice://" in command or "tv:" in command:
            url = f"{url}open"
            payload = {"url": command}
            func = self.session.post

        if func is not None:
            async with func(url, json=payload, headers=headers) as response:
                data = await response.json()
                _LOGGER.warning("Sending command %s to %s, response was: %s %s", url, payload, response.status, data)
                if response.status == 200:
                    return True
                elif response.status in (401, 403):  # Token expired, retry authentication
                    _LOGGER.warning("Session token expired, renewing...")
                    if await self.authenticate():
                        return await self.send_command(command)
                _LOGGER.error("Failed to send command %s to %s, response was: %s %s", url, payload, response.status, data)
                return False
        else:
            code_array = command.split(',')
            player_path = f"http://{self.host}/pub/remote_control?code={self.remote_code}&key="
            for code in code_array:
                async with self.session.get(player_path+code) as response:
                    if response.status != 200:
                        return False
            return True
