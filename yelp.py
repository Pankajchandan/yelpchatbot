# -*- coding: utf-8 -*-

import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode
import ConfigParser
import logging

import template

# set loggging and configs
logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

config = ConfigParser.ConfigParser()
config.read("config.ini")

# API constants
API_KEY= config.get('tokens', 'yelp_api_key')
API_HOST = config.get('url', 'yelp_api_host')
SEARCH_PATH = config.get('url', 'yelp_search')
BUSINESS_PATH = config.get('url', 'yelp_business')

# Defaults
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
DEFAULT_ACTION = 'yelp'

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    log.info(u'Querying %s ...', url)

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

def get_reviews(api_key, business_id):
    review_path = BUSINESS_PATH + business_id + '/reviews'
    return request(API_HOST, review_path, api_key)

def query_api(action=DEFAULT_ACTION, term=DEFAULT_TERM, location=DEFAULT_LOCATION):
    # serach for buisnessID
    response = search(API_KEY, term, location)
    businesses = response.get('businesses')
    
    if not businesses:
        log.info(u'No businesses for %s in %s found.',term, location)
        return

    # take the topresult
    business_id = businesses[0]['id']

    if action.lower()=='yelp':
        log.info(u' %s businesses found, querying business info ' \
            'for the top 1 result "%s" ...', len(businesses), business_id)
        response = get_business(API_KEY, business_id)
        review = get_reviews(API_KEY, business_id)

        log.info(u'Result for business "%s" found:',business_id)
    else:
        response = json.dumps({'text': 'incorrect action word'})

    return slack_packer(action, response, review)


def slack_packer(action, response, review):
    temp = dict()
    if action.lower()=='yelp':
	temp = template.SLACK_TEMPLATE
	temp['attachments'][0]['fields'][0]['value'] = response['rating']
	temp['attachments'][0]['fields'][1]['value'] = response['price']
	temp['attachments'][0]['fields'][2]['value'] = response['review_count']
	temp['attachments'][0]['fields'][3]['value'] = response['display_phone']
	temp['attachments'][0]['title'] = response['name']
    temp['attachments'][0]['title_link'] = response['url']
	temp['attachments'][0]['image_url'] = response['image_url']
	temp['attachments'][1]['author_name'] = review['reviews'][0]['user']['name']
	temp['attachments'][1]['text'] = review['reviews'][0]['text']
    temp['attachments'][1]['title_link'] = review['reviews'][0]['url']
	temp['attachments'][1]['image_url'] = review['reviews'][0]['user']['image_url']

    return temp


# for debugging purpose
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--action', dest='action', default=DEFAULT_ACTION,
                        type=str, help='action (default: %(default)s)')
    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.action, input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
