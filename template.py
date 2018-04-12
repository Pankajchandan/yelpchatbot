# -*- coding: utf-8 -*-

SLACK_TEMPLATE = dict()
SLACK_TEMPLATE = {
    u'text': 'This is a search from yelp',
    u'attachments': [
        {
            u'title': None,
            u'title_link': None,
            u'fields': [
                {
                    u'title': 'Rating',
                    u'value': None,
                    u'short': 'true'
                },
                {
                    u'title': u'Price',
                    u'value': None,
                    u'short': u'true'
                },
		{
                    u'title': u'Review count',
                    u'value': None,
                    u'short': u'true'
                },
		{
                    u'title': u'Phone Number',
                    u'value': None,
                    u'short': u'true'
                }
            ],
            u'author_name': u'Slack Yelp',
            u'author_icon': u'http://a.slack-edge.com/7f18/img/api/homepage_custom_integrations-2x.png',
            u'image_url': None
        },
        {
            u'title': u'Customer Review',
            u'title_link': None,
            u'author_name': None,
            u'author_icon': u'http://a.slack-edge.com/7f18/img/api/homepage_custom_integrations-2x.png',
            u'text': None,
            u'image_url': None
        }
    ]
}
