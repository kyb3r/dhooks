# Discord Webhooks

**_Interact with discord webhooks using python._**

This library enables you to easily format discord messages and send them to a channel using a webhook url. Synchronous requests as well as asynchronous requests are supported within the library through an easy to use API.

### Requirements:
```py
requests
aiohttp
```

### Simple Example:
```py
from dhooks import Webhook

hook = Webhook('WEBHOOK_URL')

hook.send("Hello there! I'm a webhook :open_mouth:")
```
**Results in this:**

<img src='https://i.imgur.com/3acyaiy.png'>

### Another Example:
```py
from dhooks import Webhook, Embed


hook = Webhook('WEBHOOK_URL')

embed = Embed(
    description='This is the **description** of the embed! :smiley:'
    color=0x1e0f3,
    timestamp=True # sets the timestamp to current time
    )

embed.set_author(name='Author Goes Here', icon_url='https://i.imgur.com/rdm3W9t.png')
embed.add_field(name='Test Field',value='Value of the field \U0001f62e')
embed.add_field(name='Another Field',value='1234 😄')
embed.set_footer(text='Here is my footer text', icon_url='https://i.imgur.com/rdm3W9t.png')

embed.set_thumbnail('https://i.imgur.com/rdm3W9t.png')
embed.set_image('https://i.imgur.com/f1LOr4q.png')

hook.send(embeds=embed)
```
**Results in this:**

<img src='https://i.imgur.com/8Ms4OID.png'>

# Asynchronous Usage

To asynchronously make requests using aiohttp, simply pass in `is_async=True` as a parameter when creating a Webhook object. An example is as follows.

```py
import asyncio
import dhooks

async def main():
    hook = dhooks.Webhook('WEBHOOK_URL', is_async=True)
    await hook.send('hello') # sends a message to the webhook channel

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

