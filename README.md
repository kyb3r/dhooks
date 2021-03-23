<h1 align="center">Discord Webhooks</h1>

<div align="center">
  <strong><i>Interact with discord webhooks using python.</i></strong>
  <br>
  <br>

  <a href="https://travis-ci.com/kyb3r/dhooks">
    <img src="https://img.shields.io/travis/com/kyb3r/dhooks/master.svg?style=for-the-badge&colorB=06D6A0" alt="Travis" />
  </a>
  
  <a href="https://test-dhooks-doc.readthedocs.io/en/latest/?badge=latest">
    <img src="https://img.shields.io/readthedocs/dhooks.svg?style=for-the-badge&colorB=E8BE5D" alt="Documentation Status" />
  </a>

  <a href="https://github.com/kyb3r/dhooks/">
    <img src="https://img.shields.io/pypi/pyversions/dhooks.svg?style=for-the-badge&colorB=F489A3" alt="Py Versions" />
  </a>

  <a href="https://pypi.org/project/dhooks/">
    <img src="https://img.shields.io/pypi/v/dhooks.svg?style=for-the-badge&colorB=61829F" alt="PyPi" />
  </a>

  <a href="https://github.com/kyb3r/dhooks/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/kyb3r/dhooks.svg?style=for-the-badge&colorB=7289DA" alt="LICENSE" />
  </a>
</div>
<br>

<div align="center">
  This <strong>simple</strong> library enables you to easily interact with discord webhooks, allowing you to easily format discord messages and discord embeds, retrieve webhook information, modify and delete webhooks. Asynchronous usage is also supported.
</div>

## Installation

To install the library simply use pip.

```commandline
pip install dhooks
```

If you would also like to get the latest version of dhooks from GitHub, build docs, run tests or run examples, you may want to install
dhooks with the optional extended dependencies.

```commandline
git clone https://github.com/kyb3r/dhooks.git
cd dhooks
pip install .[tests,docs,examples]
```

## Quick Start

### Sending Messages:

```python
from dhooks import Webhook

hook = Webhook('url')

hook.send("Hello there! I'm a webhook :open_mouth:")
```

<img src='https://i.imgur.com/8wu283y.png' width=300>

### Discord Embeds:

You can easily format and send embeds using this library.

<img src='https://i.imgur.com/8Ms4OID.png' width=400>

Note: `Embed` objects from `discord.py` are also compatible with this library.

```python
from dhooks import Webhook, Embed

hook = Webhook('url')

embed = Embed(
    description='This is the **description** of the embed! :smiley:',
    color=0x5CDBF0,
    timestamp='now'  # sets the timestamp to current time
    )

image1 = 'https://i.imgur.com/rdm3W9t.png'
image2 = 'https://i.imgur.com/f1LOr4q.png'

embed.set_author(name='Author Goes Here', icon_url=image1)
embed.add_field(name='Test Field', value='Value of the field :open_mouth:')
embed.add_field(name='Another Field', value='1234 :smile:')
embed.set_footer(text='Here is my footer text', icon_url=image1)

embed.set_thumbnail(image1)
embed.set_image(image2)

hook.send(embed=embed)
```

### Sending Files:

You can easily send files as shown.

```python
from dhooks import Webhook, File
from io import BytesIO
import requests

hook = Webhook('url')

file = File('path/to/file.png', name='cat.png')  # optional name for discord

hook.send('Look at this:', file=file)
```

You can also pass a file-like object:

```python
response = requests.get('https://i.imgur.com/rdm3W9t.png')
file = File(BytesIO(response.content), name='wow.png')

hook.send('Another one:', file=file)
```

### Get Webhook Info:

You can get some basic information related to the webhook through Discord's API.

```python
hook.get_info()
```

The following attributes will be populated with data from discord:

- `hook.guild_id`
- `hook.channel_id`
- `hook.default_name`
- `hook.default_avatar_url`

### Modify and Delete Webhooks:

You can change the default name and avatar of a webhook easily.

```python
with open('img.png', 'rb') as f:
    img = f.read()  # bytes

hook.modify(name='Bob', avatar=img)

hook.delete()  # webhook deleted permanently
```

### Asynchronous Usage:

To asynchronously make requests using `aiohttp`, simply use `Webhook.Async` to create the object. An example is as follows. Simply use the `await` keyword when calling API methods.

```python
from dhooks import Webhook

async def main():
    hook = Webhook.Async('url')

    await hook.send('hello')
    await hook.modify('bob')
    await hook.get_info()
    await hook.delete()

    await hook.close()  # close the client session
```

Alternatively you can use an `async with` block (asynchronous context manager) to automatically close the session once finished.

```python
async def main():
    async with Webhook.Async('url') as hook:
        await hook.send('hello')
```

## Documentation

You can find the full API reference [here](https://dhooks.readthedocs.io).

## License

This project is licensed under MIT.

## Contributing

Feel free to contribute to this project, a helping hand is always appreciated.

[Join our discord server](https://discord.gg/etJNHCQ).
