from base64 import b64encode
from dataclasses import dataclass

import aiohttp
import requests

from .embed import Embed

try:
    import ujson as json
except ImportError:
    import json


class File:

    content_type = 'application/octet-stream'

    def __init__(self, fp, name=None):
        self.fp = fp
        self.name = name or fp if isinstance(fp, str) else getattr(fp, 'name', 'file')

    def open(self):
        if isinstance(self.fp, str): # its a filepath
             self.fp = open(self.fp, 'rb')
        return self.fp
    
    def close(self):
        if not isinstance(self.fp, str):
            self.fp.close()

class Webhook:
    '''Asynchronous client that makes it easy to use webhooks'''

    ENDPOINT = 'https://discordapp.com/api/webhooks/{id}/{token}'

    def __init__(self, url=None, session=None, is_async=False, **options):
        self.id = options.get('id')
        self.token = options.get('token')
        self.username = options.get('username')
        self.avatar_url = options.get('avatar_url')
        self._url = url
        self.url = url or self.ENDPOINT.format(id=self.id, token=self.token)
        self.is_async = is_async
        self.session = session or (aiohttp.ClientSession() if is_async else requests.Session())
        self.headers = {'Content-Type': 'multipart/form-data'}
        self.default_avatar = None
        self.default_name = None
        self.guild_id = None
        self.channel_id = None

    def close(self):
        return self.session.close()

    def send(self, content=None, embeds=[], username=None, avatar_url=None, file=None, tts=False):
        '''Sends a message to the payload url'''

        payload = {
            'content': content,
            'username': username or self.username,
            'avatar_url': avatar_url or self.avatar_url,
            'tts': tts
        }

        if not hasattr(embeds, '__iter__'):  # supports a list/tuple of embeds or a single embed
            embeds = [embeds]

        payload['embeds'] = [em.to_dict() for em in embeds]
        
        return self.request('POST', payload, file=file)
    
    def modify(self, name=None, avatar=None):
        ''''''
        payload = {
            'name': name or self.username
        }

        if avatar:
            payload['avatar'] = self._bytes_to_base64_data(avatar)

        payload = {k: v for k, v in payload.items() if v}

        if not payload:
            raise ValueError('No attributes to be modified specified.')
        
        return self.request(payload, method='PATCH')

    def get_info(self):
        '''Updates self with webhook object data from the given token'''
        return self.request(method='GET')

    def delete(self):
        '''Deletes the webhook permanently'''
        return self.request(method='DELETE')

    def _update_fields(self, data):
        if 'content' in data:
            return # a message object was returned
        self.id = data.get('id')
        self.token = data.get('token')
        self.default_avatar = data.get('avatar')
        self.default_name = data.get('name')
        self.guild_id = data.get('guild_id')
        self.channel_id = data.get('channel_id')

    def request(self, method='POST', payload=None, file=None):

        if not self._url and (not self.id or not self.token):
            raise ValueError('Missing data for webhook url.')

        headers = None if file else self.headers

        payload = json.dumps(payload)
            
        if self.is_async:
            return self.async_request(method, payload, file)

        if file:
            payload = {'payload_json': payload}
            multipart = {'file': (file.name, file.open(), file.content_type)}

        resp = self.session.request(method, self.url, data=payload, headers=headers, files=multipart)
        resp.raise_for_status()
        data = self._try_json(resp.text)

        if isinstance(data, dict):
            self._update_fields(data)
            return self

        return data

    async def async_request(self, method='POST', payload=None, file=None):

        headers = None if file else self.headers

        data = payload

        if file:
            data = aiohttp.FormData()
            data.add_field('file', file.open(), filename=file.name, content_type=file.content_type)
            data.add_field('payload_json', payload)

        async with self.session.request(method, self.url, data=data, headers=headers) as resp:
            resp.raise_for_status()
            text = await resp.text()
            data = self._try_json(text)
            if isinstance(data, dict):
                self._update_fields(data)
                return self
            return data

    @staticmethod
    def _get_mime_type_for_image(data):
        if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
            return 'image/png'
        elif data.startswith(b'\xFF\xD8') and data.rstrip(b'\0').endswith(b'\xFF\xD9'):
            return 'image/jpeg'
        elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
            return 'image/gif'
        else:
            raise ValueError('Unsupported image type given')

    @staticmethod
    def _bytes_to_base64_data(data):
        fmt = 'data:{mime};base64,{data}'
        mime = Webhook._get_mime_type_for_image(data)
        b64 = b64encode(data).decode('ascii')
        return fmt.format(mime=mime, data=b64)

    @staticmethod
    def _try_json(text):
        if not text:
            return True # request successful but no response.
        return json.loads(text)
