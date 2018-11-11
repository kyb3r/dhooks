import asyncio
import traceback
import datetime
from email.utils import parsedate_to_datetime

import aiohttp
import requests

try:
    import ujson as json
except ImportError:
    import json

class Embed:
    '''Class that represents a discord embed'''

    __slots__ = (
        'color','title','url','author',
        'description','fields','image',
        'thumbnail','footer','timestamp',
        )
    
    def __init__(self, **kwargs):
        '''Initialises an Embed object'''
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.description = kwargs.get('description')
        self.timestamp = kwargs.get('timestamp')
        self.fields = kwargs.get('fields', [])
          
    def del_field(self, index: int):
        '''Deletes a field by index'''
        self.fields.pop(index)

    def set_title(self, title: str, url:str):
        self.title = title
        self.url = url
      
    def add_field(self, name: str, value: str, inline: bool=True):
        '''Adds a field'''
        field = {
            'name': name, 
            'value': value, 
            'inline': inline
            }
        self.fields.append(field)
    
    def set_author(self, name: str, icon_url: str=None, url: str=None):
        '''Sets the author of the embed'''
        self.author = {
            'name': name,
            'icon_url' : icon_url,
            'url' : url
            }
    
    def set_thumbnail(self, url: str):
        '''Sets the thumbnail of the embed'''
        self.thumbnail = {'url': url}
    
    def set_image(self, url):
        '''Sets the image of the embed'''
        self.image = {'url': url}
        
    def set_footer(self, text: str, icon_url: str=None):
        '''Sets the footer of the embed'''
        self.footer = {
            'text': text,
            'icon_url': icon_url
            }
    
    def to_dict(self) -> dict:
        '''Turns the object into a dictionary'''
        return {
            key: getattr(self, key)
            for key in self.__slots__
            if hasattr(self, key) and getattr(self, key)
            }

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

    def send(self, content: str=None, embeds: list or Embed=[], tts: bool=False) -> bool:
        '''Sends a message to the payload url'''

        payload = {
            'content': content,
            'username': self.username,
            'avatar_url': self.avatar_url,
            'tts': tts
            }

        if not hasattr(embeds, '__iter__'): # supports a list/tuple of embeds 
            embeds = [embeds]               # or a single embed

        payload['embeds'] = [em.to_dict() for em in embeds] 

        payload = json.dumps(payload, indent=4)

        if self.is_async:
            return self.async_request(payload)
        else:
            return self.request(payload)

    def request(self, payload: str) -> bool:
        resp = self.session.post(self.url, data=payload, headers=self.headers)
        resp.raise_for_status()
        return True

    async def async_request(self, payload: str) -> bool:
        async with self.session.post(self.url, data=payload, headers=self.headers) as resp:
            resp.raise_for_status()
            return True