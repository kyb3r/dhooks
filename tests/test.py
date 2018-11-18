import asyncio
import os
from dhooks import Webhook

url = os.getenv('webhook_url')

# new shortcut for making an async webhook class
hook = Webhook.Async(url)

# you can now use with statements with the Webhook class

# async code

async def main():
    '''
    Following code automatically calls await webhook.close()
    once it exits the async with block. 
    Webhook.Async(url) is a shortcut for Webhook(url, is_async=True)
    '''

    async with Webhook.Async(url) as hook:
        await hook.send('bob')

asyncio.run(main())


# Blocking code 

with Webhook(url) as hook:
    hook.send('bob')




