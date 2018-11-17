import re

import aiohttp
import requests

from .embed import Embed
from .file import File
from .utils import try_json, bytes_to_base64_data
from .utils import aliased, alias

try:
    import ujson as json
except ImportError:
    import json

@aliased
class Webhook:
    '''
    Class that represents a discord webhook

    Parameters
    ----------
    url: str, optional
        The webhook url that the client will send requests to
        Note: the url contains the id and token of the webhook in 
        the form: ``webhooks/{id}/{token}``. If you dont provide a url
        you must provide the `id` and `token` keyword arguments.
    session: requests.Session or aiohttp.ClientSession, optional
        The http session that will be used to make requests to the api.
    is_async: bool, optional
        Decides wether or not to the api methods in the class are 
        asynchronous or not, defaults to False. If set to true, 
        all api methods have the same interface, but returns a coroutine.
    \*\*id: int, optional
        The discord id of the webhook. If not provided, it will 
        be extracted from the webhook url.
    \*\*token: str, optional
        The token that belongs to the webhook. If not provided,
        it will be extracted from the webhook url.
    \*\*username: str, optional
        The username that will override the default name of the 
        webhook everytime you send a message.
    \*\*avatar_url: str, optional
        The avatar_url that will override the default avatar 
        of the webhook everytime you send a message.

    Attributes
    ----------
    default_name: str
        Note: Set to None if :meth:`get_info()` hasn't been called.
        The default name of the webhook, this can be changed via the modify
        function or directly through discord server settings.
    default_avatar: str
        Note: Set to None if :meth:`get_info()` hasn't been called.
        The default avatar string of the webhook. 
    default_avatar_url: str
        Note: Set to None if :meth:`get_info()` hasn't been called.
        The url version of the default avatar the webhook has.
    guild_id: int 
        Note: Set to None if :meth:`get_info()` hasn't been called.
        The id of the webhook's guild. (server)
    channel_id: int
        Note: Set to None if :meth:`get_info()` hasn't been called.
        The id of the channel the webhook sends messages to..
    '''

    REGEX = r'discordapp.com/api/webhooks/(?P<id>[0-9]{17,21})/(?P<token>[A-Za-z0-9\.\-\_]{60,68})'
    ENDPOINT = 'https://discordapp.com/api/webhooks/{id}/{token}'
    CDN = 'https://cdn.discordapp.com/avatars/{0.id}/{0.default_avatar}.{1}?size={2}'

    def __init__(self, url=None, is_async=False, session=None, **options):
        self.id = options.get('id')
        self.token = options.get('token')
        self.username = options.get('username')
        self.avatar_url = options.get('avatar_url')
        self.url = url or self.ENDPOINT.format(id=self.id, token=self.token)
        self._set_id_and_token(url)
        self.is_async = is_async
        self.session = session or (aiohttp.ClientSession() if is_async else requests.Session())
        self.headers = {'Content-Type': 'application/json'}
        self.default_avatar = None
        self.default_name = None
        self.guild_id = None
        self.channel_id = None

    def close(self):
        return self.session.close()

    @property
    def default_avatar_url(self):
        if not self.default_avatar: # return default image
            return 'https://cdn.discordapp.com/embed/avatars/0.png'
        return self.CDN.format(self, 'png', 1024)

    @alias('execute')
    def send(self, content=None, embeds=[], username=None, avatar_url=None, file=None, tts=False):
        '''
        Sends a message to discord through the webhook.
        
        Parameters
        ----------
        content: str, optional
            The message contents (up to 2000 characters)
        embeds: :class:`Embed` or List[:class:`Embed`]
            Embedded rich content, you can either send a single embed
            or a list of them.
        file: :class:`File`, optional
            The file that will be uploaded
        tts: bool, optional
            Wether or not the message will use text-to-speech.
            defaults to False
        username: str, optional
            Override the default username of the webhook, defaults 
            to :attr:`username`
        avatar_url: str, optional
            Override the default avatar of the webhook. defaults to
            :attr:`self.avatar_url`.

        '''

        payload = {
            'content': content,
            'username': username or self.username,
            'avatar_url': avatar_url or self.avatar_url,
            'tts': tts
        }

        if not hasattr(embeds, '__iter__'):  # supports a list/tuple of embeds or a single embed
            embeds = [embeds]

        payload['embeds'] = [em.to_dict() for em in embeds]
        
        return self._request('POST', payload, file=file)

    @alias('edit')    
    def modify(self, name=None, avatar=None):
        '''
        Edits the webhook.

        Parameters
        ----------
        name: str, optional
            The new default name of the webhook,
            defaults to :attr:`username`
        avatar: bytes, optional
            The new default avatar that webhook will be set to.
        '''
        payload = {
            'name': name or self.username
        }

        if avatar:
            payload['avatar'] = bytes_to_base64_data(avatar)

        payload = {k: v for k, v in payload.items() if v}

        if not payload:
            raise ValueError('No attributes to be modified specified.')
        
        return self._request(method='PATCH', payload=payload)

    def get_info(self):
        '''
        Updates self with data retrieved from discord.
        The following attributes are refreshed with data:
        :attr:`default_avatar`, :attr:`default_name`, :attr:`guild_id`, :attr:`channel_id`
        '''
        return self._request(method='GET')

    def delete(self):
        '''Deletes the webhook permanently'''
        return self._request(method='DELETE')

    def _request(self, method='POST', payload=None, file=None, multipart=None):
        '''
        Makes a request to the api. This function may or may 
        not be a coroutine based on the `is_async` attribute.
        '''

        headers = None if file else self.headers

        payload = json.dumps(payload)
            
        if self.is_async:
            return self._async_request(method, payload, file)

        if file:
            payload = {'payload_json': payload}
            multipart = {'file': (file.name, file.open(), file.content_type)}

        resp = self.session.request(method, self.url, data=payload, headers=headers, files=multipart)
        resp.raise_for_status()
        data = try_json(resp.text)

        if file:
            file.close()

        if isinstance(data, dict):
            self._update_fields(data)
            return self

        return data

    async def _async_request(self, method='POST', payload=None, file=None):
        '''Async version of the request function using aiohttp'''

        headers = None if file else self.headers

        data = payload

        if file:
            data = aiohttp.FormData()
            data.add_field('file', file.open(), filename=file.name, content_type=file.content_type)
            data.add_field('payload_json', payload)

        async with self.session.request(method, self.url, data=data, headers=headers) as resp:
            resp.raise_for_status()
            text = await resp.text()
            data = try_json(text)
            if file:
                file.close()
            if isinstance(data, dict):
                self._update_fields(data)
                return self
            return data
    
    def _update_fields(self, data):
        if 'content' in data:
            return # a message object was returned
        self.id = data.get('id')
        self.token = data.get('token')
        self.default_avatar = data.get('avatar')
        self.default_name = data.get('name')
        self.guild_id = data.get('guild_id')
        self.channel_id = data.get('channel_id')
    
    def _set_id_and_token(self, url):
        if not url and (not self.id or not self.token):
            raise ValueError('Missing data for webhook url.')
        if self.id and self.token:
            return
        # extract them from provided url.
        match = re.search(self.REGEX, self.url)
        if not match:
            raise ValueError('Invalid webhook url provided.')
        id, token = match.groups()
        self.id = int(id)
        self.token = token
