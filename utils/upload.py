#!/usr/bin/env python

#
# This program will upload a given folder or item from the Unlocking the 
# Airwaves AirTable database to the Internet Archive. The files for the folder 
# or item need to be zipped up, and you will need to set the AIRTABLE_KEY
# environment variable:
#
#    export AIRTABLE_KEY="thisisnottherealkey"
#    export IA_KEY="thisisnteither"
#    export IA_SECRET="thisdefinitelynotasecret"
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
IA_ACCESS_KEY = os.environ.get('IA_ACCESS_KEY')
IA_SECRET_KEY = os.environ.get('IA_SECRET_KEY')
AIRTABLE_BASE = 'https://api.airtable.com/v0/appr7YXcZfPKUF4nI/'

if not AIRTABLE_KEY:
    sys.exit("You forgot to set AIRTABLE_KEY in your environment")
if not IA_ACCESS_KEY:
    sys.exit("You forgot to set IA_ACCESS_KEY in your environment")
if not IA_SECRET_KEY:
    sys.exit("You forgot to set IA_SECRET_KEY in your environment")

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
    if 'records' in data:
        if len(data['records']) != 1:
            sys.exit('error: no such record %s %s %s' % (table, path, params))
        else:
            return data['records'][0]['fields']
    else:
        return data['fields']

def add(rec, col_name, headers, header_name, link_table=None):
    if col_name not in rec:
        return
    count = 0
    for val in rec[col_name]:
        count += 1
        if link_table:
            linked_rec = get(link_table, val)
            val = linked_rec['Name']
        h = 'x-archive-meta%02i-%s' % (count, header_name)
        headers[h] = val

def curl(id, zip_file, headers):
    cmd = [
        'curl',
        '--location',
        '--upload-file', zip_file, 
    ]
    for k in sorted(headers.keys()):
        cmd.append('--header')
        cmd.append("%s:%s" % (k, headers[k]))

    cmd.append('http://s3.us.archive.org/%s/%s' % (id, zip_file))
    return cmd


# figure out if we are working with a folder or an item

m = re.match('naeb-b(\d+)-f(\d+)(?:-(\d+))?', id)
if not m:
    sys.exit("error: invalid id %s" % id)

box_num, folder_num, item_num = m.groups()

if item_num:
    table_name = 'Contents by Item with Metadata' 
else:
    table_name = 'Contents by Folder with Metadata' 

rec = get(table_name, params={'filterByFormula': '(FIND("%s",{ID}))' % id})

headers = {

    # boilerplate headers

    'x-archive-auto-make-bucket': '1',
    'x-archive-meta-sponsor': 'National Endowment for the Humanities',
    'x-archive-meta-coordinator': 'Maryland Institute for Technlogy in the Humanities',
    'x-archive-meta-format': 'image/tiff',
    #'x-archive-meta-collection': 'mediahistory',
    'x-archive-meta-collection': 'opensource_movies',
    'x-archive-meta-language': 'eng',
    #'x-archive-meta-mediatype': 'texts',
    'x-archive-meta-mediatype': 'movies',

    # dynamic headers

    'authorization': 'LOW %s:%s' % (IA_ACCESS_KEY, IA_SECRET_KEY),
    'x-archive-meta-file': zip_file,
    'x-archive-meta-identifier': id,
    'x-archive-meta-title': rec.get('Title', ''),
    'x-archive-meta-series': rec.get('Series', ''),
    'x-archive-meta-rights': rec.get('Rights', ''),
    'x-archive-meta-description': rec.get('Description', ''),
    'x-archive-meta-folder': folder_num,
    'x-archive-meta-box': box_num,

    # these were from the example curl command but not sure how to map
    #'x-archive-meta-journal-title': 'Variety',
    #'x-archive-meta-page-count': '54'
}

# item and folder specific metadata

if item_num:
    headers['x-archive-meta-item'] = item_num
else:
    add(rec, 'Relation', headers, 'relation')

# metadata that can take multiple values

add(rec, 'Publisher', headers, 'publisher', 'Authorities (People & Entities)')
add(rec, 'Creator(s)', headers, 'creator', 'Authorities (People & Entities)')
add(rec, 'Contributor(s)', headers, 'contributor', 'Authorities (People & Entities)')
add(rec, 'Subject(s)', headers, 'subject', 'Authorities (Subjects)')
add(rec, 'Type(s)', headers, 'type')

# Date 

'''
date = rec['Date']
if re.match('\d\d\d\d-\d\d\d\d', date):
    date_string = date
    year, year_end = date.split('-')
    
--header 'x-archive-meta-year:1957' \
--header 'x-archive-meta-year-end:1957' \
--header 'x-archive-meta-date:1957' \
--header 'x-archive-meta-date-start:1957-11-06T23:23:59Z' \
--header 'x-archive-meta-date-end:1957-11-27T23:23:59Z' \
--header 'x-archive-meta-date-string:November 1957' \

--header 'x-archive-meta-year:1952' \
--header 'x-archive-meta-year-end:1953' \
--header 'x-archive-meta-date:1952-1953' \
--header 'x-archive-meta-date-start:1952-01-01T23:23:59Z' \
--header 'x-archive-meta-date-end:1953-12-31T23:23:59Z' \
--header 'x-archive-meta-date-string:1952-1953' 
'''

print(json.dumps(curl(id, zip_file, headers), indent=2))

# Coverage (Spatial)

# Coverage (Temporal)

