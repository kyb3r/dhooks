import aiohttp
import requests

from .embed import Embed

try:
    import ujson as json
except ImportError:
    import json


class Webhook:
    '''Asynchronous client that makes it easy to use webhooks'''

    def __init__(self, url: str, session=None, is_async: bool=False, **options):
        self.url = url
        self.is_async = is_async
        self.session = session or (aiohttp.ClientSession() if is_async else requests.Session())
        self.headers = {'Content-Type': 'application/json'}
        self.username = options.get('username')
        self.avatar_url = options.get('avatar_url')

    def close(self):
        self.session.close()

    def send(self, content: str = None, embeds: list or Embed = [], tts: bool = False) -> bool:
        '''Sends a message to the payload url'''

        payload = {
            'content': content,
            'username': self.username,
            'avatar_url': self.avatar_url,
            'tts': tts
        }

        if not hasattr(embeds, '__iter__'):  # supports a list/tuple of embeds or a single embed
            embeds = [embeds]

        payload['embeds'] = [em.to_dict() for em in embeds]

        payload = json.dumps(payload, indent=4)

        if self.is_async:
            return self.async_request(payload)
        else:
            return self.request(payload)

    def request(self, payload: str) -> bool:
        resp = self.session.post(self.url, data=payload, headers=self.headers)
        resp.raise_for_status()
        return resp

    async def async_request(self, payload: str) -> bool:
        async with self.session.post(self.url, data=payload, headers=self.headers) as resp:
            resp.raise_for_status()
            return resp
