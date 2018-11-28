import unittest
import requests
import os

import dhooks

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    pass


REAL_URL = os.getenv('TEST_WEBHOOK_URL')
FAKE_URL = 'https://discordapp.com/api/webhooks/12345678901234567890/' \
           'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk'

MALFORMED_URL = 'https://discordapp.com/api/webhooks/bob'


class TestBlockingClient(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()

    def test_send_content(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            dhooks.Webhook(FAKE_URL, session=self.session).send('TEST')

        try:
            dhooks.Webhook(REAL_URL, session=self.session).send('TEST')
        except requests.exceptions.HTTPError:
            self.fail("Valid client failed to send.")

    # TODO: Add test for invalid urls
