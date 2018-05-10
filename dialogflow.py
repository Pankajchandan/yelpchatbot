import argparse
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
import apiai

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')
config = ConfigParser.ConfigParser()
config.read("config.ini")

CLIENT_ACCESS_TOKEN = config.get('tokens', 'dialog_key')
DEFAULT_QUERY = 'where to dine in san jose, ca'

def dialogflow_api(query=DEFAULT_QUERY):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  
    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    request.query = query
    response = json.loads(request.getresponse().read().decode('utf-8'))
    log.info("printing response from dialogflow")
    log.debug(pprint.pformat(response))
    pprint.pprint(response)
    message1 = response['result']['parameters']['Restaurant'][0]
    message2 = response['result']['parameters']['location'][0]['city']
    confidence = response['result']['score']
    return message1,message2,confidence

# for debugging purpose
def main():
    """
    >>> python dialogflow.py --query 'where to dine in san jose'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', dest='query', default=DEFAULT_QUERY,
                        type=str, help='action (default: %(default)s)')
    input_values = parser.parse_args()

    try:
        rest, city, conf = dialogflow_api(input_values.query)
        log.info("location returned: %s", city)
        log.info("term returned: %s", rest)
        log.info("confidence: %s", conf)
    except Exception as msg:
        log.error("%s", msg)

if __name__=="__main__":
    main()
