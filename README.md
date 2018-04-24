# Discord-Webhooks
Discord webhook embeds made easy with Python

[![Join the developers on Discord](https://discordapp.com/api/guilds/427220922496450561/widget.png?style=banner2)](https://discord.gg/hPUxaJ4)

### Requirements:

```py
requests
```

### Simple Example:

```py
from discord_hooks import Webhook

url = 'WEBHOOK_URL'

msg = Webhook(url,msg="Hello there! I'm a webhook :open_mouth:")

msg.post()
```

**Results in this:**

![Simple webook result](https://i.imgur.com/3acyaiy.png)

### All Parameters:

```py
embed = Webhook(url, color=int, msg=str) # NOTE: the `msg` kwarg is a normal message.

embed.set_author(name=str, icon=url, url=url) # NOTE: the `url` kwarg is the url when you click on the author.
embed.set_title(title=str, url=url)
embed.add_field(name=str, value=str, inline=bool) # NOTE: If you leave `inline` out, it defaults to `True`
embed.del_field(index)
embed.set_thumbnail(url)
embed.set_image(url)
embed.set_footer(text=str,icon=url,ts=True) # NOTE: You can input `True` (current time) or an int timestamp.


embed.post() # Formats the object into a valid json object and then posts it to the webhook url
```

### Another Example:

```py
from discord_hooks import Webhook

url = 'WEBHOOK_URL'

embed = Webhook(url, color=123123)

embed.set_author(name='Author Goes Here', icon='https://i.imgur.com/rdm3W9t.png')
embed.set_desc('This is the **description** of the embed! :smiley:')
embed.add_field(name='Test Field',value='Value of the field :open_mouth:')
embed.add_field(name='Another Field',value='1234 :smile:')
embed.set_thumbnail('https://i.imgur.com/rdm3W9t.png')
embed.set_image('https://i.imgur.com/f1LOr4q.png')
embed.set_footer(text='Here is my footer text',icon='https://i.imgur.com/rdm3W9t.png',ts=True)

embed.post()
```

**Results in this:**

![Advanced webhook result](https://i.imgur.com/8Ms4OID.png)
