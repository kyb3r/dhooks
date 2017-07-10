from Webhooks import Webhook


url = open('url').read()

msg = Webhook(url,msg="Hello there! I'm a webhook \U0001f62e")

msg.post()
