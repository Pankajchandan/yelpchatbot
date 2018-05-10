# -*- coding: utf-8 -*-

"""
This is app.py that runs the http server. This runs
as a process on heroku cloud infrastructure
"""


import os
import sys
import json
import logging
from datetime import datetime
import requests
from flask import Flask, request, Response
import ConfigParser
import pprint
import coloredlogs

from yelp import query_api
from dialogflow import dialogflow_api

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)                  
log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')
config = ConfigParser.ConfigParser()
config.read("config.ini")

SLACK_URL = config.get('url','slack')
SLACK_VARIFY_TOKEN = config.get('tokens', 'slack_verify_token')


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
        terms, location = None, None

        if args[0].lower() == 'yelp':
            log.info("calling dialogflow api")
            try:
                term, location, conf = dialogflow_api(args[1:])
            except Exception as e:
                pass
            log.info("calling yelp api..")
            if terms != None and location != None:
                slack_payload = query_api(args[0], term, location)
            else:
                slack_payload = query_api(args[0], args[1], ' '.join(args[2:]))
        else:
            slack_payload = {u'text': u'invalid action word'}

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
        '\n'.join('{}: {}'.format(k, v) for k, v in req.form.to_dict().items()),
    ))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

