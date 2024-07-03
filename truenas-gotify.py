#!/usr/bin/env python3
import os
import sys
from aiohttp import web
from aiohttp import ClientSession

# The url the alerts should be forwarded to.
# Format: http[s]://{host}:{port}/
GOTIFY_BASEURL = os.environ.get("GOTIFY_URL")
# The token for the gotify application
# Example: cGVla2Fib29v
GOTIFY_TOKEN = os.environ.get("GOTIFY_TOKEN")

LISTEN_HOST = "127.0.0.1"
PORT = 31662


routes = web.RouteTableDef()

# Listen to post requests on / and /message
@routes.post("/")
@routes.post("/message")
async def on_message(request):
    content = await request.json()
    # The content of the alert message
    message = content["text"]
    print("===== Alert =====")
    print(message)

    # Forward the alert to gotify
    gotify_resp = await send_gotify_message(message, GOTIFY_TOKEN)

    # Return the gotify status code to truenas
    return web.Response(status=gotify_resp.status)

# Send an arbitrary alert to gotify
async def send_gotify_message(message, token, title=None, priority=None):
    # URL parameters
    params = {"token": token}
    # POST body
    json = {"message": message}

    # Optional gotify features
    if title:
        json["title"] = title
    if priority:
        json["priority"] = priority

    async with ClientSession() as session:
        async with session.post(GOTIFY_BASEURL, params=params, json=json) as resp:
            return resp


if __name__ == "__main__":
    # Check if env variable is set
    if GOTIFY_BASEURL == None:
        sys.exit("Set Gotify Endpoint via 'GOTIFY_URL=http[s]://{host}:{port}/'!")
    if GOTIFY_TOKEN == None:
        sys.exit("Set Gotify App Token via 'GOTIFY_TOKEN={token}'!")

    # Add /message to the url
    if not "message" in GOTIFY_BASEURL:
        if not GOTIFY_BASEURL[-1] == "/":
            GOTIFY_BASEURL += "/"
        GOTIFY_BASEURL += "message"


    # Listen on default port
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=LISTEN_HOST, port=PORT)
