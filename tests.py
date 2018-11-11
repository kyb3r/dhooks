import os

from dhooks import Embed, Webhook

webhook_url = os.getenv('webhook_url')

client = Webhook(webhook_url)

client.send('testing')

embed = Embed()
embed.color = 0x00FF00
embed.description = "this description supports [named links](https://discordapp.com) as well. ```\nyes, even code blocks```"
embed.timestamp = "2018-04-30T05:34:26-07:00"

embed.set_author(name='Author Goes Here', icon_url='https://i.imgur.com/rdm3W9t.png', url='https://discordapp.com/')
embed.set_title(title='title ~~(did you know you can have markdown here too?)~~', url='https://discordapp.com/')

embed.add_field(name="Field 1 :smiley:", value="some of these properties have certain limits...", inline=False)
embed.add_field(name="Field 2 😱", value="try exceeding some of them!",inline=False)
embed.add_field(name="Field 3 🙄", value="Jokes, dont do that.",inline=False)
embed.add_field(name="Field 4 🙄", value="these last two")
embed.add_field(name="Field 5 🙄", value="are inline fields")

embed.set_thumbnail('https://cdn.discordapp.com/embed/avatars/0.png')
embed.set_image('https://cdn.discordapp.com/embed/avatars/0.png')
embed.set_footer(text='Time Stamp is here =>', icon_url='https://cdn.discordapp.com/embed/avatars/0.png')

client.send(embeds=embed)