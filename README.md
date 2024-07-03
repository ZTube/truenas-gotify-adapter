# TrueNas Gotify Adapter

TrueNas does not natively provide a way to send alerts and notifications to a Gotify server. This repo 'abuses' the TrueNas Slack alert integration and provides a fake slack webhook endpoint to forward alerts to a Gotify server.
Note that Slack is not required at all for this integration to work.

## Installation
1. Apps -> Discover Apps -> Custom App
  - Enter an Application Name, e.g. "truenas-gotify"
  - _Image Repository_: ghcr.io/ztube/truenas-gotify-adapter
  - _Image Tag_: main
  - Environment Variables:
    - _Name_: GOTIFY_URL
    - _Value_: [your gotify url] e.g.https://gotify.example.com/
    - _Name_: GOTIFY_TOKEN
    - _Value_: [your gotify app token] e.g. cGVla2Fib29v

  - Check _"Provide access to node network namespace for the workload"_
  - Save

1. System Settings -> Alert Settings -> Add
  - _Type_: Slack
  - _Webhook URL_: http://localhost:31662
  - Click _Send Test Alert_ to test the connection
  - Save
