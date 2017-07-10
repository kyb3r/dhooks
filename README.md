# Discord-Webhooks
#### *Discord Webhook Embeds for Python*

### Example:
```py
from Webhooks import Webhook

url = open('url').read()

embed = Webhook(url, color=123123)

embed.set_author(name='Author Goes Here', icon='https://i.imgur.com/rdm3W9t.png')
embed.set_desc('This is the **description** of the embed! \U0001f603 ')
embed.add_field(name='Test Field',value='Value of the field \U0001f62e')
embed.add_field(name='Another Field',value='1234 😄')
embed.set_thumbnail('https://i.imgur.com/rdm3W9t.png')
embed.set_image('https://i.imgur.com/f1LOr4q.png')
embed.set_footer(text='Here is my footer text',icon='https://i.imgur.com/rdm3W9t.png',ts=True)

embed.post()
```
**Results in this:**

<img src='https://i.imgur.com/8Ms4OID.png'>

### All Parameters:

```py
embed = Webhook(url, color=int, msg=str) # NOTE: the `msg` kwarg is a normal message.
embed.set_author(name=str, icon=url, url=url) # NOTE: the `url` kwarg is the url when you click on the author.
embed.set_title(title=str, url=url) 
embed.add_field(name=str, value=str, inline=bool) # NOTE: If you leave the `inline` kwarg out, it defaults to `True`
embed.del_field(index)
embed.set_thumbnail(url) 
embed.set_image(url)
embed.set_footer(text=str,icon=url,ts=bool or int) # NOTE: ts = timestamp, you can either input `True` (current time) or an integer timestamp.

```py
