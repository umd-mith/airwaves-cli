#!/usr/bin/env python

#
# This program will upload a given folder or item from the Unlocking the 
# Airwaves AirTable database to the Internet Archive. The files for the folder 
# or item need to be zipped up, and you will need to set the AIRTABLE_KEY
# environment variable:
#
#    export AIRTABLE_KEY="thisisnottherealkey"
#    ./upload.py naeb-b072-f01 naeb-b072-f01.zip
#
# You'll notice that this is just a kludgy wrapper around curl, which is already
# being used by the Wisconsin Historical Society's workflow with Internet 
# Archive. Since these uploads can be quite large and take some time it was 
# decided to keep using curl instead of using Python directly for the HTTP
# POST so as not to introduce more possibilities for error. Also we wanted it
# to work with stock python2.7 that comes with OS X. So no fancy extra
# libraries. That explains at least some of the kludginess.
#

import os
import re
import sys
import json
import urllib
import urllib2
import subprocess

AIRTABLE_KEY = os.environ.get('AIRTABLE_KEY')
AIRTABLE_BASE = 'https://api.airtable.com/v0/appr7YXcZfPKUF4nI/'

if not AIRTABLE_KEY:
    sys.exit("You forgot to set AIRTABLE_KEY in your environment")

if len(sys.argv) != 3:
    sys.exit("usage: upload.py <id> <file.zip>")

id, zip_file = sys.argv[1:3]

def get(table, path=None, params=None):
    url = AIRTABLE_BASE + urllib.quote(table)
    if path:
        url += '/' + path
    if params:
        url += '?' + urllib.urlencode(params)
    req = urllib2.Request(url)
    req.add_header('Authorization', 'Bearer %s' % AIRTABLE_KEY)
    resp = urllib2.urlopen(req)
    data = json.load(resp)
    if len(data['records']) != 1:
        sys.exit('error: no such record %s %s %s' % (table, path, params))
    return data['records'][0]

# figure out if we are working with a folder or an item

m = re.match('naeb-b(\d+)-f(\d+)(?:-(\d+))?', id)
if not m:
    sys.exit("error: invalid id %s" % id)

box_num, folder_num, item_num = m.groups()

if item_num:
    table_name = 'Contents by Item with Metadata' 
else:
    table_name = 'Contents by Folder with Metadata' 

# get the metadata for the thing

r = get(table_name, params={'filterByFormula': '(FIND("%s",{ID}))' % id})

# 

'''
'x-archive-meta-sponsor:Media History Digital Library' \
'x-archive-meta-contributor:Media History Digital Library' \
'x-archive-meta-coordinator:Media History Digital Library' \
'x-archive-meta-journal-title:Variety' \
'x-archive-meta-title:Variety (November 1957)' \
'x-archive-meta-file:variety208-1957-11_images.zip' \
'x-archive-meta-volume:208' \
'x-archive-meta-year:1957' \
'x-archive-meta-year-end:1957' \
'x-archive-meta-date:1957' \
'x-archive-meta-date-start:1957-11-06T23:23:59Z' \
'x-archive-meta-date-end:1957-11-27T23:23:59Z' \
'x-archive-meta-date-string:November 1957' \
'x-archive-meta-page-count:335' \
'x-archive-meta-publisher:New York, NY: Variety Publishing Company' \
'x-archive-meta-source:Microfilm' \
'x-archive-meta-creator:Variety' \
'x-archive-meta-format:Periodicals' \
'x-archive-meta-microfilm-contributor:Library of Congress National Audio Visual Conservation Center' \
'x-archive-meta-collection:mediahistory' \
'x-archive-meta01-sub-collection:Theatre and Vaudeville' \
'x-archive-meta02-sub-collection:Hollywood Studio System' \
'x-archive-meta03-sub-collection:Recorded Sound' \
'x-archive-meta04-sub-collection:Broadcasting' \
'x-archive-meta01-subject:Motion Pictures' \
'x-archive-meta02-subject:Recorded Sound' \
'x-archive-meta03-subject:Vaudeville' \
'x-archive-meta04-subject:Theatre' \
'x-archive-meta05-subject:Broadcasting' \
'x-archive-meta-language:eng' \
'x-archive-meta-mediatype:texts' \
'authorization: LOW fTbpqdwH1hTXQZXE:P7r68yrN5JXVRynC' \
'''

# follow foreign keys

'''
curl --location \
--header 'x-archive-auto-make-bucket:1' \
--header 'x-archive-meta-identifier:variety208-1957-11' \
--header 'x-archive-meta-sponsor:Media History Digital Library' \
--header 'x-archive-meta-contributor:Media History Digital Library' \
--header 'x-archive-meta-coordinator:Media History Digital Library' \
--header 'x-archive-meta-journal-title:Variety' \
--header 'x-archive-meta-title:Variety (November 1957)' \
--header 'x-archive-meta-file:variety208-1957-11_images.zip' \
--header 'x-archive-meta-volume:208' \
--header 'x-archive-meta-year:1957' \
--header 'x-archive-meta-year-end:1957' \
--header 'x-archive-meta-date:1957' \
--header 'x-archive-meta-date-start:1957-11-06T23:23:59Z' \
--header 'x-archive-meta-date-end:1957-11-27T23:23:59Z' \
--header 'x-archive-meta-date-string:November 1957' \
--header 'x-archive-meta-page-count:335' \
--header 'x-archive-meta-publisher:New York, NY: Variety Publishing Company' \
--header 'x-archive-meta-source:Microfilm' \
--header 'x-archive-meta-creator:Variety' \
--header 'x-archive-meta-format:Periodicals' \
--header 'x-archive-meta-microfilm-contributor:Library of Congress National Audio Visual Conservation Center' \
--header 'x-archive-meta-collection:mediahistory' \
--header 'x-archive-meta01-sub-collection:Theatre and Vaudeville' \
--header 'x-archive-meta02-sub-collection:Hollywood Studio System' \
--header 'x-archive-meta03-sub-collection:Recorded Sound' \
--header 'x-archive-meta04-sub-collection:Broadcasting' \
--header 'x-archive-meta01-subject:Motion Pictures' \
--header 'x-archive-meta02-subject:Recorded Sound' \
--header 'x-archive-meta03-subject:Vaudeville' \
--header 'x-archive-meta04-subject:Theatre' \
--header 'x-archive-meta05-subject:Broadcasting' \
--header 'x-archive-meta-language:eng' \
--header 'x-archive-meta-mediatype:texts' \
--header 'authorization: LOW fTbpqdwH1hTXQZXE:P7r68yrN5JXVRynC' \
--upload-file variety208-1957-11_images.zip \http://s3.us.archive.org/variety208-1957-11/variety208-1957-11_images.zip
'''

#print(json.dumps(get('Authorities (People & Entities)', 'rectCByrOPGPG7xAR'), indent=2))
#print(json.dumps(get('Contents by Item with Metadata', params={'filterByFormula': '(FIND("%s",{ID}))' % id}), indent=2))
