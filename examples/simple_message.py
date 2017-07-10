from Webhooks import Webhook


url = open('url').read()

msg = Webhook(url, msg="Hello There :)")

msg.post()
