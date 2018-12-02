# Asynchronous example with Sanic
import socket

import aiohttp
from sanic import Sanic, response

from dhooks import Webhook, Embed

###
webhook_url = "<INSERT WEBHOOK URL HERE>"
###

app = Sanic(__name__)


@app.listener('before_server_start')
async def init(app, loop):
    """Sends a message to the webhook channel when server starts."""
    app.session = aiohttp.ClientSession(loop=loop)  # to make web requests
    app.webhook = Webhook.Async(webhook_url, session=app.session)

    em = Embed(color=0x2ecc71)
    em.set_author('[INFO] Starting Worker')
    em.description = 'Host: {}'.format(socket.gethostname())

    await app.webhook.send(embed=em)


@app.listener('after_server_stop')
async def server_stop(app, loop):
    """Sends a message to the webhook channel when server stops."""
    em = Embed(color=0xe67e22)
    em.set_footer('Host: {}'.format(socket.gethostname()))
    em.description = '[INFO] Server Stopped'

    await app.webhook.send(embed=em)
    await app.session.close()


@app.get('/')
async def index(request):
    return response.text("To send a message, go to "
                         "0.0.0.0:8000/message/?msg='insert message here'.")


@app.get('/message')
async def message(request):
    """
    To send a message, go to 0.0.0.0:8000/message/?msg='insert message here'.
    """

    msg = request.get('msg')
    if msg is None:
        return request.text("To send a message, go to 0.0.0.0:8000/"
                            "message/?msg='insert message here'.")
    await app.webhook.send(msg)
    return response.text("Send.")

if __name__ == "__main__":
    # visit 0.0.0.0:8000/ from your browser
    app.run(host="0.0.0.0", port=8000)
