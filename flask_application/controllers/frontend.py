#!/usr/bin/env python

import datetime

from flask import Blueprint, request, render_template
from flask_application import app
import requests
import bs4
import xmltodict
import os

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    if app.debug:
        app.logger.debug('rendering index')
    '''lets get on the index a proper xml fed to json'''

    r = requests.get('http://jobs.code4lib.org/feed/')

    '''probably should not convert to string, but we just want
       to make sure we are getting it.'''
    #feed = unicode(str(bs4.BeautifulSoup(r.content)), 'utf-8')

    #print type(bs4.BeautifulSoup(r.content))

    feed = xmltodict.parse(r.content)

    '''we can now dig into the xml like >>>feed['feed']['entry'][0]['title']'''

    for i in range(0, len(feed['feed']['entry'])):
        #print i, ') '
        #for key in feed['feed']['entry'][i]:
            
        #    print key, ' +++ ', feed['feed']['entry'][i][key], ' \n '
        #print '##############################################'
        #print feed['feed']['entry'][i] + '\n'
        print feed['feed']['entry'][i]['title']
        print feed['feed']['entry'][i]['employer']
        print feed['feed']['entry'][i]['link'][0]['@href']
        '''ahhhh, why cant we get location and georss:point and location nodes??? 
           because not all records have them:('''
        if feed['feed']['entry'][i].has_key('location'):
            print feed['feed']['entry'][i]['location']
        if feed['feed']['entry'][i].has_key('georss:point'):
            print feed['feed']['entry'][i]['georss:point'] 

    '''TODO: Turn the above into a JSON stream, using all relevant pages of the feed 
        (not just the first).'''
        



    # o = open('tmp.out', 'w')
    # outStr = ''
    # for result in feed:
    #     for key in feed[result]:
    #         print key, ': \n ', feed[result][key]
    #         outStr += str(key) + ': \n ' + str(feed[result][key]) + '\n'

    #     o.write(outStr)
    # o.close()

    return render_template(
                'index.html',
                config=app.config,
                now=datetime.datetime.now,
                feed=feed,
            )

