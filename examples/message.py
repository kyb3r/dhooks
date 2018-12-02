from dhooks import Webhook


###
webhook_url = "<INSERT WEBHOOK URL HERE>"
###


hook = Webhook(webhook_url)
hook.send("Hello there! I'm a webhook :open_mouth:")
