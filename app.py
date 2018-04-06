import os
import sys
import json
import logging
from datetime import datetime
import requests
from flask import Flask, request
import ConfigParser

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)                                                  
log = logging.getLogger(__name__)
config = ConfigParser.ConfigParser()
config.read("config.ini")

SLACK_URL = config.get('url','slack')
DIALOG_URL = config.get('url','dialog')
YELP_URL = config.get('url','yelp')

@app.route('/', methods=['GET'])
def verify():
    return 'service is up'


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log.debug("%s", data)

    slack_payload = {
        "text": "test"
        }
    return Response(json.dumps(slack_payload), status=200, mimetype='application/json')


def send_message(url, message):

    payload={"channel": "#yelpbot", 
        "username": "YELP",
        "text": message_text,
        }

    response = requests.post(url,json=message)
    if response.status_code != 200:
        log.info("message successfully sent")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

