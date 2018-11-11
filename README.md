# Discord-Webhooks
#### *Discord Webhook Embeds for Python*

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

