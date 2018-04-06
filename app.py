import os
import sys
import json
import logging
from datetime import datetime
import requests
from flask import Flask, request, Response
import ConfigParser

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)                                                  
log = logging.getLogger(__name__)
config = ConfigParser.ConfigParser()
config.read("config.ini")

SLACK_URL = config.get('url','slack')
DIALOG_URL = config.get('url','dialog')
YELP_URL = config.get('url','yelp')
SLACK_VARIFY_TOKEN = config.get('tokens', 'slack_verify_token')

@app.route('/', methods=['GET'])
def verify():
    return 'service is up'


@app.route('/', methods=['POST'])
def webhook():
    if SLACK_VARIFY_TOKEN == request.form.get('token'):
        text = request.form.get('text')
        log.debug("text: %s",text)

        # intent = get_intent(DIALOG_URL, text)
        # if valid intent:
        # reco = get_reco(YELP_URL, text)
        # else reco = fallback(text)

        slack_payload = {
            "text": "test"
            }
        return Response(json.dumps(slack_payload), status=200, mimetype='application/json')
    else:
        log.warning("message from unknown sources")


def get_intent(url, text):
    payload = {
        }
    res = requests.post(url,json=message)
    if res.status_code != 200:
        log.error("error sending message sent")

    return intent


def get_yelp(url, text):
    payload = {
        }
    res = requests.post(url, json=message)
    return reco


def fallback(text):
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

