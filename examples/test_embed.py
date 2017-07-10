from discordWebhooks import Webhook

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
