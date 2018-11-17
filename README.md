
<h1 align="center">Discord Webhooks</h1>

<div align="center">
    <strong><i>Interact with discord webhooks using python.</i></strong>
</div>
<br>
<div align="center">
    This <strong>simple</strong> library enables you to easily format discord messages and send them to a channel using a webhook url. Synchronous requests as well as asynchronous requests are supported within the library through an easy to use API.
</div>




### Installation
To install the library simply use [pipenv](http://pipenv.org/) (or pip, of course).

```
pipenv install dhooks
```

### Sending Messages:

<img src='https://i.imgur.com/8wu283y.png' align='right' width='380' height='125'>

```py
from dhooks import Webhook

hook = Webhook('WEBHOOK_URL')

hook.send("Hello there! I'm a webhook :open_mouth:")
```

### Sending Files:
You can easily send files as shown.
```
from dhooks import Webhook, File
import requests
import io

hook = Webhook('WEBHOOK_URL')

file = File('path/to/file.png', name='cat.png') # optional name for discord

hook.send('Look at this', file=file)

# you can also pass in a File like object

response = await requests.get('https://i.imgur.com/rdm3W9t.png')
file = File(io.BytesIO(response.content), name='wow.png')

hook.send('Another one', file=file)
```

### Discord Embeds:
You can easily format and send embeds using this library. [**Result**](https://i.imgur.com/8Ms4OID.png)
```py
from dhooks import Webhook, Embed

hook = Webhook('WEBHOOK_URL')

embed = Embed(
    description='This is the **description** of the embed! :smiley:'
    color=0x1e0f3,
    timestamp=True # sets the timestamp to current time
    )
   
image1 = 'https://i.imgur.com/rdm3W9t.png'
image2 = 'https://i.imgur.com/f1LOr4q.png'

embed.set_author(name='Author Goes Here', icon_url=image1)
embed.add_field(name='Test Field',value='Value of the field \U0001f62e')
embed.add_field(name='Another Field',value='1234 😄')
embed.set_footer(text='Here is my footer text', icon_url=image1)

embed.set_thumbnail(image1)
embed.set_image(image2)

hook.send(embeds=embed)
```

### Get Webhook Info
You can get some basic information related to the webhook through Discord's api.

```py
hook.get_info()

# the following attributes will be populated with data from discord.

hook.guild_id, hook.channel_id, hook.default_name, hook.default_avatar_url 
```

### Modify and Delete Webhooks
You can change the default name and avatar of a webhook easily.
```py
with open('img.png', rb) as f:
    img = f.read() # bytes like object
    
hook.modify(name='Bob', avatar=img) 

hook.delete() # Webhook deleted permanently
```

### Asynchronous Usage:

To asynchronously make requests using aiohttp, simply pass in `is_async=True` as a parameter when creating a Webhook object. An example is as follows. Simply use the `await` keyword when calling api methods.

```py
import asyncio
from dhooks import Webhook

async def main():
    hook = Webhook('WEBHOOK_URL', is_async=True)
    await hook.send('hello') # sends a message to the webhook channel

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### License
This project is licensed under MIT

### Contributing
Feel free to contribute to this project, a helping hand is always appreciated.

