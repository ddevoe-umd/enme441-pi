# Use HTTP POST to create a webhook to send a message
# to a Discord channel

# Here we just want to send a simple POST request to a
# fixed target IP, without managing the entire HTTP
# communication process as with sockets.  To do this we
# can use the Python requests module

from time import sleep
import requests
import json
from RPi import GPIO

p = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.IN)

# On Discord, do the following:
# 1. create a channel
# 2. create a webhook for the channel (select channel -> gear icon
#     -> Integrations -> Webhooks)
# 3. get the URL for the webhook, it should look something like this:
url = 'https://discord.com/api/webhooks/1002267352513134712/jn5EabAyrVLC2SYTNq6a2F_ySJcmvHj1QlT9ODHNK1fTFyEmS1wVxbXoDrDzd-VzNLOG'

while True:
    # For Discord webhook formatting see:
    # https://discord.com/developers/docs/resources/webhook
    # (scroll down to "Execute Webhook" section). At a minimum
    # a "content" field is required. We can also override the
    # default webhook user by adding a "username" field:
    data = json.dumps(
        {'content' : str(GPIO.input(p)),
         'username': "ENME441 bot"}   )
    result = requests.post(url, headers = {'content-type': 'application/json'}, data=data)  # send the POST request
    print(result.text)                      # and print the response
    sleep(10)

