import unittest
import requests
import os

import dhooks
from io import BytesIO

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    load_dotenv = find_dotenv = None


REAL_URL = os.getenv('TEST_WEBHOOK_URL')
FAKE_URL = 'https://discordapp.com/api/webhooks/12345678901234567890/' \
           'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk'

MALFORMED_URL = 'https://discordapp.com/api/webhooks/bob'


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

        self.real_webhook = dhooks.Webhook(REAL_URL)

        response = requests.get('https://i.imgur.com/rdm3W9t.png')
        self.file = dhooks.File(BytesIO(response.content), name='wow.png')

    def test_fake_url(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            with dhooks.Webhook(FAKE_URL) as wh:
                wh.send("TEST")

    def test_send_content(self):
        try:
            with dhooks.Webhook(REAL_URL) as wh:
                wh.send('TEST')
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")

    def test_send_embed(self):
        try:
            with dhooks.Webhook(REAL_URL) as wh:
                wh.send(embed=self.embed)
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")

    def test_send_file(self):
        try:
            with dhooks.Webhook(REAL_URL) as wh:
                wh.send(file=self.file)
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")

    def test_send_content_embed(self):
        try:
            with dhooks.Webhook(REAL_URL) as wh:
                wh.send('TEST', embed=self.embed)
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")

    def test_send_content_file(self):
        try:
            with dhooks.Webhook(REAL_URL) as wh:
                wh.send('TEST', file=self.file)
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")

    def test_send_embed_file(self):
        try:
            with dhooks.Webhook(REAL_URL) as wh:
                wh.send(embed=self.embed, file=self.file)
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")

    def test_send_content_embed_file(self):
        try:
            with dhooks.Webhook(REAL_URL) as wh:
                wh.send(content="TEST", embed=self.embed, file=self.file)
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")
