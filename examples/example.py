from discord_hooks import Webhook
WEBHOOK_URL = 'ADD YOUR WEBHOOK URL HERE'

embed = Webhook(
    url=WEBHOOK_URL,
    username='Hello World!',
    color=1234123)
embed.set_author(name='Author Goes Here', icon='https://i.imgur.com/rdm3W9t.png', url='https://discordapp.com/')
embed.set_title(title='title ~~(did you know you can have markdown here too?)~~', url='https://discordapp.com/')
embed.set_desc("this description supports [named links](https://discordapp.com) as well. ```\nyes, even code blocks```")
embed.add_field(name="Field 1 \U0001f603", value="some of these properties have certain limits...",inline=False)
embed.add_field(name="Field 2 😱", value="try exceeding some of them!",inline=False)
embed.add_field(name="Field 3 🙄", value="Jokes, dont do that.",inline=False)
embed.add_field(name="Field 4 🙄", value="these last two")
embed.add_field(name="Field 5 🙄", value="are inline fields")
embed.set_thumbnail('https://cdn.discordapp.com/embed/avatars/0.png')
embed.set_image('https://cdn.discordapp.com/embed/avatars/0.png')
embed.set_footer(text='Time Stamp is here =>',ts=True,icon='https://cdn.discordapp.com/embed/avatars/0.png')

embed.post()
