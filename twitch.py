import aiohttp
import asyncio
import json

class TwitchAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    async def authenticate(self):
        url = "https://id.twitch.tv/oauth2/token"
        async with aiohttp.ClientSession() as session:
            params = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }
            async with session.post(url, params=params) as resp:
                data = await resp.json()
                self.token = data["access_token"]

    async def get_stream_data(self, usernames):
        if not self.token:
            await self.authenticate()

        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}"
        }
        params = [("user_login", name) for name in usernames]

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                data = await resp.json()
                return data.get("data", [])
