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
IA_KEY = os.environ.get('IA_KEY')
IA_SECRET = os.environ.get('IA_SECRET')
AIRTABLE_BASE = 'https://api.airtable.com/v0/appr7YXcZfPKUF4nI/'

if not AIRTABLE_KEY:
    sys.exit("You forgot to set AIRTABLE_KEY in your environment")
if not IA_KEY:
    sys.exit("You forgot to set IA_KEY in your environment")
if not IA_SECRET:
    sys.exit("You forgot to set IA_SECRET in your environment")

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

'x-archive-auto-make-bucket:1' \
'x-archive-meta-sponsor:National Endowment for the Humanities' \
'x-archive-meta-coordinator:Maryland Institute for Technlogy in the Humanities'

'x-archive-meta-identifier:variety208-1957-11'
'x-archive-meta-journal-title:Variety' \
'x-archive-meta-file:variety208-1957-11_images.zip' \
'authorization: LOW %s:%s' % (IA_KEY, IA_SECRET)

# Folder

# Title x-archive-meta-title

# Series

# Digitize?

# Date

# Creator(s)

# Contributor(s)

# Subject(s)

# Coverage (Spatial)

# Coverage (Temporal)

# Type(s)

# Format

# Relation

# Description

# Publisher

# Rights

# Collection

# Notes

# Attachments


# Item

# Title Series

# Date

# Creator(s)

# Contributor(s)

# Subject(s)

# Coverage (Spatial)

# Coverage (Temporal)

# Type(s)

# Format

# Relation

# Description

# Publisher

# Rights

# Collection

# Notes

# 


# follow foreign keys

'''
curl --location \
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
--upload-file variety208-1957-11_images.zip \http://s3.us.archive.org/variety208-1957-11/variety208-1957-11_images.zip
'''

'''
  {
    "contributor": [
      "Wisconsin Historical Society",
      "Cooperstein, Edwin",
      "Underwood, Robert Jr.",
      "Vogl, Dick",
      "Harrison, Burt",
      "Seidner, Fred J",
      "Webster Jones, Lewis",
      "Chase Smith, Margaret",
      "White, Lynn Jr.",
      "The Public Relations Board",
      "Nelson, Don",
      "Educational and Television Radio Center",
      "Hill, Harold E.",
      "Stanley, Ray",
      "Crary, Ryland",
      "WTIC (Hartford, CT)",
      "Wisconsin Historical Society",
      "Connecticut Council for the Advancement of Economic Education",
      "Wass, Philmore B.",
      "Trocchi, Doris R.",
      "Carpenter, Russell F.",
      "Rich, Carla",
      "Goodman, Robert C.",
      "Paulu, Burton",
      "Easton, Alan G.",
      "Skornia, Harry J.",
      "US Army Infantry Center, Information Section",
      "Steffensen, James L., Jr.",
      "Newburn, Harry K.",
      "Lyons, Roger",
      "Michelfelder, Phyllis",
      "Von Hallberg, Gene",
      "Fostervoll, Kaare",
      "Schweitzer, Albert",
      "Latimer, Ira H.",
      "Oldfield, Barney",
      "American Women in Radio & Television, Inc.",
      "Kerr, Edith",
      "Renick, Helen Prokloff",
      "Bennett, H.W.",
      "National Education Program",
      "Wheeldon, DelVina",
      "Dale, Edgar",
      "Kirkpatrick, Evron M.",
      "Bardos, Arthur",
      "Dahlgren, E.G. \"Ty\"",
      "AB Maskin & Electro",
      "Pellandini, Carlo",
      "Spears, Richard L.",
      "Eblen, Cliff",
      "Thompson, William G., Jr.",
      "Teven, Irwin K.",
      "Heim, Paul K.",
      "Laundauer, Ernest",
      "Burt, Hardy",
      "Rider, Richard",
      "Iwasaki, Kohei",
      "Fenz, Roland E."
    ],
    "coordinator": "Maryland Institute for Technology in the Humanities and University of Wisconsin-Madison Department of Communication Arts",
    "creator": "National Association of Educational Broadcasters",
    "date": "1958",
    "date-end": "1958-12-31T23:23:59Z",
    "date-start": "1958-01-01T23:23:59Z",
    "date-string": "1958",
    "description": "1958 Correspondence and documentation regarding program content submissions to the NAEB Network. Both NAEB Member and non-member representatives from various universities and other organizations correspondence with the NAEBs Bob Underwood (Network Manager) and Harold Hill (Associate Director).",
    "file": "naeb-b072-f01_images.zip",
    "format": "image/tiff",
    "language": "eng",
    "page-count": "289",
    "publisher": "Wisconsin Historical Society",
    "rights": "Wisconsin Historical Society",
    "series": "Subject File",
    "sponsor": "National Endowment for the Humanities",
    "title": "NAEB Programs, Proposals, 1958",
    "year": "1958",
    "year-end": "1958",
    "mediatype": "texts",
    "relation": [
      "References Science and Society",
      "References Living America",
      "References Barnard Forum (1958)",
      "References Stretching Your Family Income",
      "References Queen of Battle",
      "References Language and Music",
      "References Conversations Abroad",
      "References Science and Secondary Education",
      "References Peace and Atomic War",
      "References Britain and the United Nations",
      "References Let's Talk It Over",
      "References What's Ahead for Higher Education?",
      "References The Friendly Philosopher",
      "References What Kind of America Do We Want?",
      "References The Atom and You",
      "References This Woman's World",
      "References Yale Reports",
      "References Living with Languages",
      "References Britain Views the United Nations",
      "References The American Adventure",
      "References Neuvieme Symphonie de Beethoven",
      "References A Time to Remember",
      "References Latin America Views the United Nations",
      "References Life and the World"
    ],
    "subject": [
      "National Educational Radio Network (NERN)",
      "Programming"
    ],
    "type": [
      "Text",
      "Correspondence"
    ],
    "publicdate": "2018-06-26 15:32:40",
    "uploader": "erhoyt@gmail.com",
    "addeddate": "2018-06-26 15:32:40",
    "identifier-access": "http://archive.org/details/naeb-b072-f01",
    "identifier-ark": "ark:/13960/t3vt8kn07",
    "imagecount": "290",
    "ocr": "ABBYY FineReader 11.0 (Extended OCR)"
  }
'''

#print(json.dumps(get('Authorities (People & Entities)', 'rectCByrOPGPG7xAR'), indent=2))
#print(json.dumps(get('Contents by Item with Metadata', params={'filterByFormula': '(FIND("%s",{ID}))' % id}), indent=2))
