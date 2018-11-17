import unittest
import requests
import os

import dhooks
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

VALID_URL = os.getenv('webhook_url')
INVALID_URL = os.getenv('webhook_url') + '55'
MALFORMED_URL = 'https://discordapp.com/api/webhooks/bob'

class TestBlockingClient(unittest.TestCase):
    def setUp(self):
        session = requests.Session()
        self.valid_client = dhooks.Webhook(VALID_URL, session=session)
        self.invalid_client = dhooks.Webhook(INVALID_URL, session=session)

    def test_send_content(self):
        send = self.valid_client.send('TEST')
        self.assertIs(send, None)

if __name__ == '__main__':
    unittest.main()
