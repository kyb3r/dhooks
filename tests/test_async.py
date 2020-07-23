import unittest
import aiohttp
import requests
import os

import dhooks
from io import BytesIO
import asyncio

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


REAL_URL = os.getenv('TEST_WEBHOOK_URL', None)
if REAL_URL is None:
    raise ValueError("TEST_WEBHOOK_URL environment variable not found.")

FAKE_URL = 'https://discord.com/api/webhooks/12345678901234567890/' \
           'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk'

MALFORMED_URL = 'https://discord.com/api/webhooks/bob'


class TestBlockingClient(unittest.TestCase):

    def setUp(self):
        self.embed = dhooks.Embed(
            description='This is the **description** of the embed! :smiley:',
            color=0x1e0f3,
            timestamp=""  # sets the timestamp to current time
        )

        image1 = 'https://i.imgur.com/rdm3W9t.png'
        image2 = 'https://i.imgur.com/f1LOr4q.png'

        self.embed.set_author(name='Author Goes Here', icon_url=image1)
        self.embed.add_field(name='Test Field',
                                  value='Value of the field :open_mouth:')
        self.embed.add_field(name='Another Field', value='1234 :smile:')
        self.embed.set_footer(text='Here is my footer text',
                                   icon_url=image1)

        self.embed.set_thumbnail(image1)
        self.embed.set_image(image2)

        response = requests.get('https://i.imgur.com/rdm3W9t.png')
        self.file = dhooks.File(BytesIO(response.content), name='wow.png')

        self.func = None

    def tearDown(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.func())

    def test_fake_url(self):
        async def main():
            with self.assertRaises(
                    aiohttp.client_exceptions.ClientResponseError):
                async with dhooks.Webhook.Async(FAKE_URL) as wh:
                    await wh.send("TEST")
        self.func = main

    def test_get_info(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.get_info()
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Failed to get info.")
        self.func = main

    def test_send_content(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.send('TEST')
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Valid client failed to send.")
        self.func = main

    def test_send_embed(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.send(embed=self.embed)
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Valid client failed to send.")
        self.func = main

    def test_send_file(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.send(file=self.file)
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Valid client failed to send.")
        self.func = main

    def test_send_content_embed(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.send('TEST', embed=self.embed)
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Valid client failed to send.")
        self.func = main

    def test_send_content_file(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.send('TEST', file=self.file)
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Valid client failed to send.")
        self.func = main

    def test_send_embed_file(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.send(embed=self.embed, file=self.file)
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Valid client failed to send.")
        self.func = main

    def test_send_content_embed_file(self):
        async def main():
            try:
                async with dhooks.Webhook.Async(REAL_URL) as wh:
                    await wh.send(content="TEST", embed=self.embed,
                                  file=self.file)
            except aiohttp.client_exceptions.ClientResponseError:
                self.fail("Valid client failed to send.")
        self.func = main
