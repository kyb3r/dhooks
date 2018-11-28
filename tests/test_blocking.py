import unittest
import requests
import os

import dhooks
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REAL_URL = os.getenv('WEBHOOK_URL')
FAKE_URL = 'https://discordapp.com/api/webhooks/12345678901234567890/abcdefghi' \
              'jklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk'

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


if __name__ == '__main__':
    unittest.main()
