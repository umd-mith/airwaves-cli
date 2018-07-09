#!/usr/bin/env python

#
# This program will upload a given folder or item from the Unlocking the 
# Airwaves AirTable database to the Internet Archive. The files for the folder 
# or item need to be zipped up. 
#
#    ./upload.py --airtable-key abc --ia-access-key def --ia-access-secret ghi naeb-b072-f01 naeb-b072-f01.zip
#
# If you would rather not have to repeat the various keys set them in your
# environment:
#
#    export AIRTABLE_KEY="thisisnottherealkey"
#    export IA_KEY="thisisnteither"
#    export IA_SECRET="thisdefinitelynotasecret"
#

import os
import re
import sys
import json
import logging
import optparse
import requests

AIRTABLE_BASE = 'https://api.airtable.com/v0/appr7YXcZfPKUF4nI/'


def main():
    env = os.environ.get
    parser = optparse.OptionParser('upload.py <id> <zip_file>')
    parser.add_option('--airtable-key', default=env('AIRTABLE_KEY'))
    parser.add_option('--ia-access-key', default=env('IA_ACCESS_KEY'))
    parser.add_option('--ia-secret-key', default=env('IA_SECRET_KEY'))
    parser.add_option('--verbose', '-v', action='store_true')
    parser.add_option('--log', default='upload.log')
    opts, args = parser.parse_args()

    # set up logging
    logging.basicConfig(filename=opts.log, level=logging.INFO)

    # check we have API keys
    if not opts.airtable_key:
        sys.exit("You forgot to set the airtable key")
    if not opts.ia_access_key:
        sys.exit("You forgot to set ia access key")
    if not opts.ia_secret_key:
        sys.exit("You forgot to set ia secret key")

    if len(args) != 2:
        parser.error('You must supply an folder/item id and a zip file path')

    id, zip_file = args

    # determine the airtable table to query using the id pattern
    if re.match('^naeb-b\d+-f\d+$', id):
        table_name = 'Contents by Folder with Metadata' 
    elif re.match('^naeb-b\d+-f\d+-\d+$', id):
        table_name = 'Contents by Item with Metadata' 
    else:
        sys.exit("error: invalid id %s" % id)

    # fetch the metadata from airtable
    rec = get_record(
        opts.airtable_key,
        table_name, 
        params={'filterByFormula': '(FIND("%s",{ID}))' % id}
    )

    # use the metadata to generate HTTP headers to POST to archive.org
    headers = get_headers(id, zip_file, rec, opts)

    url = upload(id, zip_file, headers)
    if url:
        print("created %s" % url)
    else:
        print("failed to upload. check %s for details" % opts.log)

def get_record(key, table, path=None, params=None):
    url = AIRTABLE_BASE + table
    if path:
        url += '/' + path
    headers = {'Authorization': 'Bearer %s' % key} 
    data = requests.get(url, headers=headers, params=params).json()
    if 'records' in data:
        if len(data['records']) != 1:
            sys.exit('error: no such record %s %s %s' % (table, path, params))
        else:
            return data['records'][0]['fields']
    else:
        return data['fields']


def get_headers(id, zip_file, rec, opts):
    airtable_key = opts.airtable_key
    headers = {
        # boilerplate headers
        'x-archive-auto-make-bucket': '1',
        'x-archive-meta-sponsor': 'National Endowment for the Humanities',
        'x-archive-meta-coordinator': 'Maryland Institute for Technlogy in the Humanities',
        'x-archive-meta-format': 'image/tiff',
        'x-archive-meta-collection': 'mediahistory',
        'x-archive-meta-language': 'eng',
        'x-archive-meta-mediatype': 'texts',

        # dynamic headers
        'Authorization': 'LOW %s:%s' % (opts.ia_access_key, opts.ia_secret_key),
        'x-archive-meta-file': zip_file,
        'x-archive-meta-identifier': id,
        'x-archive-meta-title': rec.get('Title', ''),
        'x-archive-meta-series': rec.get('Series', ''),
        'x-archive-meta-rights': rec.get('Rights', ''),
        'x-archive-meta-description': rec.get('Description', ''),

        # XXX: these were from the example curl command but not sure how to map
        #'x-archive-meta-journal-title': 'Variety',
        #'x-archive-meta-page-count': '54'

        # XXX: these are in the airtable but i'm not sure what ia metadata
        # Coverage (Spatial)
        # Coverage (Temporal)
    }

    # set box, folder and item
    if 'Item #' in rec:
        headers['x-archive-meta-item'] = rec['Item #']
        if 'Box and Folder #' not in rec:
            sys.exit('item %s is not linked to a folder' % id)
        folder_id = rec['Box and Folder #'][0]
        # need to get the linked folder to determine the box and folder
        folder = get_record(opts.airtable_key, 'Contents by Folder with Metadata', folder_id)
        headers['x-archive-meta-box'] = folder.get('Box', '')
        headers['x-archive-meta-folder'] = folder.get('Folder', '')
    else:
        headers['x-archive-meta-box'] = rec.get('Box', '')
        headers['x-archive-meta-folder'] = rec.get('Folder', '')

    # metadata that can take multiple values
    add_multi(airtable_key, rec, 'Publisher', headers, 'publisher', 'Authorities (People & Entities)')
    add_multi(airtable_key, rec, 'Creator(s)', headers, 'creator', 'Authorities (People & Entities)')
    add_multi(airtable_key, rec, 'Contributor(s)', headers, 'contributor', 'Authorities (People & Entities)')
    add_multi(airtable_key, rec, 'Subject(s)', headers, 'subject', 'Authorities (Subjects)')
    add_multi(airtable_key, rec, 'Type(s)', headers, 'type')

    # XXX: only folders have relations that are of interest for IA
    if 'Item #' not in rec:
        add_multi(airtable_key, rec, 'Relation', headers, 'relation')

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
    return headers


def add_multi(airtable_key, rec, col_name, headers, header_name, link_table=None):
    if col_name not in rec:
        return
    count = 0
    for val in rec[col_name]:
        count += 1
        if link_table:
            linked_rec = get_record(airtable_key, link_table, val)
            val = linked_rec['Name']
        h = 'x-archive-meta%02i-%s' % (count, header_name)
        headers[h] = val


def upload(id, zip_file, headers):
    url = 'http://s3.us.archive.org/%s/%s' % (id, zip_file)
    logging.info('uploading %s to %s', zip_file, url)
    logging.info('metadata: %s', headers)
    try:
        with open(zip_file, 'rb') as fh:
            resp = requests.put(url, headers=headers, data=fh)
            if resp.status_code == 200:
                return 'http://s3.us.archive.org/%s' % id
            else:
                logging.error('upload failed: %s', resp.status_code)
                logging.info('response headers: %s', resp.headers)
                logging.info('response content: %s', resp.text)
                return None
    except Exception as e:
        logging.error('upload failed: %s', e)
        return None


if __name__ == "__main__":
    main()

