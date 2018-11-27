# Asynchronous example usecase with sanic (Dummy app)
import os
import socket

import aiohttp
from sanic import Sanic, response

from dhooks import Webhook, Embed

app = Sanic(__name__)


@app.listener('before_server_start')
async def init(app, loop):
    """Sends a message to the webhook channel when server stops"""
    app.session = aiohttp.ClientSession(loop=loop)  # to make web requests
    app.webhook = Webhook.Async(
        os.getenv('webhook_url'),
        session=app.session
    )

    em = Embed(color=0x2ecc71)
    em.set_author('[INFO] Starting Worker')
    em.set_footer('Host: {}'.format(socket.gethostname()))

    await app.webhook.send(embeds=em)


@app.listener('after_server_stop')
async def server_stop(app, loop):
    """Sends a message to the webhook channel when server stops"""
    em = Embed(color=0xe67e22)
    em.set_footer('Host: {}'.format(socket.gethostname()))
    em.set_author('[INFO] Server Stopped')

    await app.webhook.send(embeds=em)
    await app.session.close()


@app.get('/')
async def index(request):
    return response.text('hello')


@app.get('/message')
async def message(request):
    """?msg=your message goes here"""
    msg = request.raw_args.get('msg')
    await app.webhook.send(msg)
    return response.json({'msg': msg})

if __name__ == "__main__":
    app.run()
