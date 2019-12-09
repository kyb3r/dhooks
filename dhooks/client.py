import re

import aiohttp
import requests
from typing import Union, List, Optional, Coroutine
import time
import asyncio

from .utils import bytes_to_base64_data
from .utils import aliased, alias
from .embed import Embed
from .file import File

try:
    import ujson as json
except ImportError:
    import json


@aliased
class Webhook:
    """Class that represents a Discord webhook.

    Parameters
    ----------
    url: str, optional
        The webhook URL that the client will send requests to.
        
        Note: the URL should contain the :attr:`id` and :attr:`token`
        of the webhook in the form of: ::
        
            https://discordapp.com/api/webhooks/webhooks/{id}/{token}
            
        .. warning::
            If you don't provide :attr:`url`, you must provide both :attr:`id`
            and :attr:`token` keyword arguments.

    session: requests.Session or aiohttp.ClientSession, optional
        The HTTP session that will be used to make requests to the API. If
        :attr:`session` is not provided, a new :class:`requests.Session` or
        :class:`aiohttp.ClientSession` will be created,
        depending on :attr:`is_async`.

    is_async: bool, optional
        Defaults to :class:`False`.
        Whether or not to the API methods in the class should be asynchronous.
        If set to :class:`True`, all methods will have the same interfaces,
        but returns a coroutine.

    \*\*id: int, optional
        The Discord ID of the webhook. If not provided, it will be extracted
        from the webhook URL.

    \*\*token: str, optional
        The Discord token of the webhook. If not provided, it will be
        extracted from the webhook URL.

    \*\*username: str, optional
        The username that will override the default name of the webhook every
        time you send a message.

    \*\*avatar_url: str, optional
        The URL of the avatar that will override the default avatar of the
        webhook every time you send a message.
        
    Attributes
    ----------
    id: int
        The Discord ID of the webhook.
        
    token: str
        The Discord token of the webhook.
        
    url: str
        The webhook URL that the client will send requests to.

    username: str
        The username that will override the default name of the webhook every
        time you send a message. If :attr:`username` is not provided,
        the default name is used.
        
    avatar_url: str
        The avatar URL that will override the default avatar of the webhook
        every time you send a message. If :attr:`avatar_url` is not provided,
        the default avatar is used.
        
    is_async: bool
        Whether or not to the API methods in the class should be asynchronous.
        If set to :class:`True`, all methods will have the same interfaces,
        but returns a coroutine.
        
    session: requests.Session or aiohttp.ClientSession
        The HTTP session that will be used to make requests to the API.
        :attr:`session` will be a :class:`requests.Session` or
        :class:`aiohttp.ClientSession` depending on :attr:`is_async`.
        
    default_name: str
        .. warning::
            In order for some attributes to be filled, :meth:`get_info()`
            must be called prior.
            
        The default name of the webhook, this can be changed via
        :meth:`modify` or directly through discord server settings.

    default_avatar: str
        The `avatar string <https://discordapp.com/developers/docs/re
        sources/user#avatar-data>`_ of the webhook.

    guild_id: int
        Defaults to -1.
        The id of the webhook's guild.
        
    channel_id: int
        Defaults to -1.
        The id of the channel the webhook sends messages to.

    """  # noqa: W605
    URL_REGEX = r'^(?:https?://)?((canary|ptb)\.)?discordapp\.com/api/webhooks/' \
                r'(?P<id>[0-9]+)/(?P<token>[A-Za-z0-9\.\-\_]+)/?$'
    ENDPOINT = 'https://discordapp.com/api/webhooks/{id}/{token}'
    CDN = r'https://cdn.discordapp.com/avatars/' \
          r'{0.id}/{0.default_avatar}.{1}?size={2}'

    def __init__(self, url: str = '',
                 session: Union[aiohttp.ClientSession, requests.Session,
                                None] = None,
                 is_async: bool = False,
                 **options):

        self.url = url
        self.id = options.get('id', -1)
        self.token = options.get('token', '')

        if not self.url and (self.id == -1 or not self.token):
            raise ValueError("Either url, or id and token must be provided.")

        elif not self.url and (self.id or self.token):
            raise ValueError("url and (id or token) must not be both "
                             "provided.")

        self.username = options.get('username', '')
        self.avatar_url = options.get('avatar_url', '')

        self._parse_or_format_url()

        self.is_async = is_async

        if session is not None:
            self.session = session
            if is_async and not isinstance(self.session,
                                           aiohttp.ClientSession):
                raise TypeError("is_async is set to True, but session "
                                "isn't aiohttp.ClientSession.")
            elif not is_async and not isinstance(self.session,
                                                 requests.Session):
                raise TypeError("is_async is set to False, but session "
                                "isn't requests.Session.")

        else:
            if self.is_async:
                self.session = aiohttp.ClientSession()
            else:
                self.session = requests.Session()

        self.default_name = ''
        self.default_avatar = ''
        self.guild_id = -1
        self.channel_id = -1

    @classmethod
    def Async(cls, url: str = '', session:
              Optional[aiohttp.ClientSession] = None,
              **options) -> 'Webhook':
        """
        Returns a new instance of Webhook with :attr:`is_async` set
        to :class:`True`.

        Equivalent to: ::

            Webhook(url, session=session, is_async=True, **options)
            
        """

        return cls(url, session=session, is_async=True, **options)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    def close(self):
        return self.session.close()

    @property
    def default_avatar_url(self) -> str:
        if not self.default_avatar:  # return default image
            return 'https://cdn.discordapp.com/embed/avatars/0.png'
        return self.CDN.format(self, 'png', 1024)

    @alias('execute')
    def send(self, content: str = '',
             embed: Optional[Embed] = None,
             embeds: Optional[List[Embed]] = None,
             file: Optional[File] = None,
             username: str = '',
             avatar_url: str = '',
             tts: bool = False) -> 'Webhook':
        """
        Sends a message to discord through the webhook.

        Parameters
        ----------
        content: str, optional
            The message contents (up to 2000 characters)

        embed: :class:`Embed`, optional
            Single embedded rich content.

        embeds: List[:class:`Embed`], optional
            List of embedded rich content.

        file: :class:`File`, optional
            The file that will be uploaded.

        tts: bool, optional
            Defaults to :class:`False`.
            Whether or not the message will use text-to-speech.

        username: str, optional
            Defaults to :attr:`username`.
            Override the default username of the webhook.

        avatar_url: str, optional
            Defaults to :attr:`avatar_url`.
            Override the default avatar of the webhook.

        """

        payload = {
            'tts': tts
        }

        username = username if username else self.username
        avatar_url = avatar_url if avatar_url else self.avatar_url

        if content:
            payload['content'] = content

        if username:
            payload['username'] = username

        if avatar_url:
            payload['avatar_url'] = avatar_url

        if embeds is None:
            embeds = []
            if embed is not None:
                embeds.append(embed)
        else:
            if embed is not None:
                raise ValueError("embed and embeds cannot both be set.")

        if not content and not embeds and not file:
            raise ValueError("One of content, embed/embeds, "
                             "or file must be set")
        payload['embeds'] = [em.to_dict() for em in embeds]

        return self._request('POST', payload, file=file)

    @alias('edit')
    def modify(self, name: str = '',
               avatar: bytes = b"") -> 'Webhook':
        """Edits the webhook.

        Parameters
        ----------
        name: str, optional
            The new default name of the webhook.

        avatar: bytes, optional
            The new default avatar that webhook will be set to.

        """
        payload = {}

        if name:
            payload['name'] = name

        if avatar:
            payload['avatar'] = bytes_to_base64_data(avatar)

        if not payload:
            raise ValueError('No attributes to modify.')

        return self._request(method='PATCH', payload=payload)

    def get_info(self) -> 'Webhook':
        """
        Updates :class:`Webhook` with fresh data retrieved from discord.

        The following attributes are retrieved and updated:

            * :attr:`default_avatar`
            * :attr:`default_name`
            * :attr:`guild_id`
            * :attr:`channel_id`

        """
        return self._request(method='GET')

    def delete(self) -> None:
        """
        Deletes the :class:`Webhook` permanently.

        """
        self._request(method='DELETE')

    def _request(self, method: str = 'POST', payload: dict = None,
                 file: Optional[File] = None, headers: dict = None) -> \
            Union[Optional['Webhook'], Coroutine[Optional['Webhook'],
                                                 None,
                                                 Optional['Webhook']]]:
        """
        Makes a request to the API. This function may or may
        not be a coroutine based on the :attr:`is_async` attribute.

        """
        if self.is_async:
            return self._async_request(method, payload, file, headers)

        # type annotation support for Python 3.5
        self.session = self.session  # type: requests.Session

        if payload is None:
            payload = {}

        if headers is None:
            headers = {}

        rate_limited = True
        resp = None

        while rate_limited:
            if method == "POST":
                if file is not None:
                    payload = {'payload_json': json.dumps(payload)}
                    multipart = {'file': (file.name, file.fp)}
                    resp = self.session.post(self.url, data=payload,
                                             headers=headers, files=multipart)
                else:
                    headers['Content-Type'] = 'application/json'
                    resp = self.session.post(self.url, json=payload,
                                             headers=headers)

            elif method == "DELETE":
                resp = self.session.delete(self.url, headers=headers)

            elif method == "PATCH":
                resp = self.session.patch(self.url, json=payload,
                                          headers=headers)

            elif method == "GET":
                resp = self.session.get(self.url, headers=headers)

            else:
                raise ValueError("Bad method: {}".format(method))

            if resp.status_code == 429:  # Too many request
                time.sleep(resp.json()['retry_after'] / 1000.0)
                if file is not None:
                    file.seek()
                continue
            else:
                if file is not None:
                    file.close()
                rate_limited = False

        if resp.status_code == 204:  # method DELETE
            return

        resp.raise_for_status()

        self._update_fields(resp.json())
        return self

    async def _async_request(self, method: str = 'POST',
                             payload: dict = None,
                             file: Optional[File] = None,
                             headers: dict = None) -> \
            Optional['Webhook']:
        """
        Async version of the request function using aiohttp.

        """
        # type annotation support for Python 3.5
        self.session = self.session  # type: aiohttp.ClientSession

        if payload is None:
            payload = {}

        if headers is None:
            headers = {}

        rate_limited = True
        resp = None

        while rate_limited:
            if method == "POST":
                if file is not None:
                    data = aiohttp.FormData()
                    data.add_field('file', file.fp, filename=file.name)
                    data.add_field('payload_json', json.dumps(payload))

                    resp = await self.session.post(self.url,
                                                   data=data,
                                                   headers=headers)

                else:
                    headers['Content-Type'] = 'application/json'
                    resp = await self.session.post(self.url,
                                                   json=payload,
                                                   headers=headers)

            elif method == "DELETE":
                resp = await self.session.delete(self.url,
                                                 headers=headers)

            elif method == "PATCH":
                resp = await self.session.patch(self.url,
                                                json=payload,
                                                headers=headers)

            elif method == "GET":
                resp = await self.session.get(self.url,
                                              headers=headers)

            else:
                raise ValueError("Bad method: {}".format(method))

            if resp.status == 429:  # Too many request
                await asyncio.sleep((await resp.json())
                                    ['retry_after'] / 1000.0)
                if file is not None:
                    file.seek()
                continue
            else:
                if file is not None:
                    file.close()
                rate_limited = False

        if resp.status == 204:  # method DELETE
            return

        resp.raise_for_status()

        self._update_fields(await resp.json())
        return self

    def _update_fields(self, data: dict) -> None:
        if 'content' in data:
            return  # a message object was returned
        self.id = data.get('id', self.id)
        self.token = data.get('token', self.token)
        self.default_avatar = data.get('avatar', self.default_avatar)
        self.default_name = data.get('name', self.default_name)
        self.guild_id = data.get('guild_id', self.guild_id)
        self.channel_id = data.get('channel_id', self.channel_id)

    def _parse_or_format_url(self) -> None:
        if not self.url:
            self.url = self.ENDPOINT.format(id=self.id, token=self.token)
        else:
            match = re.match(self.URL_REGEX, self.url)
            if match is None:
                raise ValueError('Invalid webhook URL provided.')

            self.id = int(match.group("id"))
            self.token = match.group("token")
