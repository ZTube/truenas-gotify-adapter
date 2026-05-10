FROM alpine:latest

RUN apk add --update --no-cache python3 py3-aiohttp

WORKDIR /app
COPY truenas-gotify.py ./

HEALTHCHECK --start-period=5s CMD wget --spider -nv -t 1 http://127.0.0.1:31662/health

CMD ["/usr/bin/env", "python3", "-u", "truenas-gotify.py"]
