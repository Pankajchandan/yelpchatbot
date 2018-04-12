# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
from datetime import datetime
import requests
from flask import Flask, request, Response
import ConfigParser
import pprint

from yelp import query_api

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)                                                  
log = logging.getLogger(__name__)
config = ConfigParser.ConfigParser()
config.read("config.ini")

SLACK_URL = config.get('url','slack')
SLACK_VARIFY_TOKEN = config.get('tokens', 'slack_verify_token')

TRIGGER_WORDS = set('yelp')


@app.route('/', methods=['GET'])
def verify():
    return 'service is up'


@app.route('/', methods=['POST'])
def webhook():
    """
    This is the default POST webhook
    """
    log.info("request recieved from slack...")
    pretty_print_POST(request)
    if SLACK_VARIFY_TOKEN == request.form.get('token'):
        text = request.form.get('text')
        args = text.split()
        
        # call dialogflow to getkeywords

        if args[0].lower() == 'yelp':
            slack_payload = query_api(args[0], args[1], ' '.join(args[2:]))
        else:
            slack_payload = {u'text': u'invalid action word'}
        
        log.info("printing the JSON sent to slack")
        log.debug(pprint.pformat(slack_payload))

        return Response(json.dumps(slack_payload), status=200, mimetype='application/json')
    else:
        log.warning("message from unknown sources")


def pretty_print_POST(req):
    """
    This method takes a request and print
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

