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

# The ip address the service should listen on
# Defaults to localhost for security reasons
LISTEN_HOST = os.environ.get("LISTEN_HOST", "127.0.0.1")
PORT = 31662


routes = web.RouteTableDef()

# Listen to post requests on / and /message
@routes.post("/")
@routes.post("/message")
async def on_message(request):
    content = await request.json()
    # The content of the alert message
    message = content["text"].strip()
    print("=========== NOTIFICATION ===========")
    print(message)
    print("========= NOTIFICATION END =========")

    # Forward the alert to gotify
    gotify_resp = await send_gotify_message(message, GOTIFY_TOKEN)

    # Check for http reponse status code 'success'
    if gotify_resp.status == 200:
        print(">> Forwarded successfully\n")
    elif gotify_resp.status in [400, 401, 403]:
        print(f">> Unauthorized! Token GOTIFY_TOKEN='{GOTIFY_TOKEN}' is incorrect\n")
    else:
        print(f">> Unknown error while forwarding to gotify. Error Code {gotify_resp.status}")

    # Return the gotify status code to truenas
    return web.Response(status=gotify_resp.status)

# Send an arbitrary alert to gotify
async def send_gotify_message(message, token, title=None, priority=None):
    # Set token through header
    headers = {"X-Gotify-Key": token}
    # POST body
    json = {"message": message}

    # Optional gotify features
    if title:
        json["title"] = title
    if priority:
        json["priority"] = priority

    async with ClientSession() as session:
        async with session.post(GOTIFY_BASEURL, headers=headers, json=json) as resp:
            return resp

if __name__ == "__main__":
    # Check if env variables are set
    if GOTIFY_BASEURL == None:
        sys.exit("Set Gotify Endpoint via 'GOTIFY_URL=http[s]://{host}:{port}/'!")
    if GOTIFY_TOKEN == None:
        sys.exit("Set Gotify App Token via 'GOTIFY_TOKEN={token}'!")

    # Add /message to the url
    if not "message" in GOTIFY_BASEURL:
        if not GOTIFY_BASEURL[-1] == "/":
            GOTIFY_BASEURL += "/"
        GOTIFY_BASEURL += "message"

    # Listen
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=LISTEN_HOST, port=PORT)
