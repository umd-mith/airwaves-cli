#!/usr/bin/env python

import re
import sys
import json
import click
import logging
import datetime
import requests

from requests.utils import quote
from airwaves.config import get_config

AIRTABLE_BASE = 'https://api.airtable.com/v0/appjfPJhxo9IHh8ld/'

def main(id, zip_file):
    config = get_config()

    # determine the airtable table to query using the id pattern
    if re.match(r'^naeb-b.?+-f.+?-\d+$', id):
        table_name = 'Document Metadata-Items'
    elif re.match(r'^naeb-b.+?-f.+$', id):
        table_name = 'Document Metadata-Folders'
    else:
        sys.exit("error: invalid id %s" % id)

    # fetch the metadata from airtable
    rec = get_record(
        config['airtable-key'],
        table_name, 
        params={'filterByFormula': '(FIND("%s",{ID}))' % id}
    )

    # use the metadata to generate HTTP headers to POST to archive.org
    headers = get_headers(id, zip_file, rec, config)

    url = upload(id, zip_file, headers)
    if url:
        print("created %s" % url)
    else:
        print("failed to upload. check log for details")

def get_record(key, table, path=None, params=None):
    logging.info('getting record from airtable for table=%s path=%s params=%s', 
            table, path, params)
    url = AIRTABLE_BASE + quote(table, safe='')
    if path:
        url += '/' + quote(path, safe='')
    headers = {'Authorization': 'Bearer %s' % key} 
    data = requests.get(url, headers=headers, params=params).json()
    logging.info('got record data %s', data)
    if 'records' in data:
        if len(data['records']) != 1:
            sys.exit('error: no such record %s %s %s' % (table, path, params))
        else:
            return data['records'][0]['fields']
    else:
        print(data)
        return data['fields']


def get_headers(id, zip_file, rec, config):
    airtable_key = config['airtable-key']
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
        'Authorization': 'LOW %(ia-access-key)s:%(ia-secret-key)s' % config,
        'x-archive-meta-file': zip_file,
        'x-archive-meta-identifier': id,
        'x-archive-meta-title': rec.get('Title', ''),
        'x-archive-meta-series': rec.get('Series', ''),
        'x-archive-meta-rights': rec.get('Rights', ''),
        'x-archive-meta-description': rec.get('Description', ''),

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
        folder = get_record(airtable_key, 'Dublin Core Metadata (Paper-Folders)', folder_id)
        headers['x-archive-meta-box'] = folder['Box']
        headers['x-archive-meta-folder'] = folder['Folder']
    else:
        headers['x-archive-meta-box'] = rec['Box']
        headers['x-archive-meta-folder'] = rec['Folder']

    # metadata that can take multiple values
    add_multi(airtable_key, rec, 'Publisher', headers, 'publisher', 'Authorities (People & Corporate Bodies)')
    add_multi(airtable_key, rec, 'Creator(s)', headers, 'creator', 'Authorities (People & Corporate Bodies)')
    add_multi(airtable_key, rec, 'Contributor(s)', headers, 'contributor', 'Authorities (People & Corporate Bodies)')
    add_multi(airtable_key, rec, 'Subject(s)', headers, 'subject', 'Authorities (Subjects)')
    add_multi(airtable_key, rec, 'Type(s)', headers, 'type')
    add_multi(airtable_key, rec, 'Coverage (Spatial)', headers, 'coverage_spatial', 'Authorities (Geographic/Locations)')

    # XXX: only folders have relations that are of interest for IA
    if 'Item #' not in rec:
        add_multi(airtable_key, rec, 'Relation', headers, 'relation')

    add_date(rec, headers)

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
                item_url = 'http://s3.us.archive.org/%s' % id
                logging.info('created %s', item_url)
                return item_url
            else:
                logging.error('upload failed: %s', resp.status_code)
                logging.info('response headers: %s', resp.headers)
                logging.info('response content: %s', resp.text)
                return None
    except Exception as e:
        logging.error('upload failed: %s', e)
        return None


def add_date(rec, headers={}):
    date = rec['Date']

    # e.g. 1920-1925
    m = re.match(r'^(\d\d\d\d)-(\d\d\d\d)$', date)
    if m:
        year_start, year_end = m.groups()
        headers['x-archive-meta-year'] = year_start
        headers['x-archive-meta-year-end'] = year_end
        headers['x-archive-meta-date'] = year_start
        headers['x-archive-meta-date-string'] = date
        headers['x-archive-meta-date-start'] = '%s-01-01T00:00:00Z' % year_start
        headers['x-archive-meta-date-end'] = '%s-12-31T23:59:59Z' % year_end


    # e.g. 1920
    m = re.match(r'^(\d\d\d\d)$', date)
    if m:
        headers['x-archive-meta-year'] = date
        headers['x-archive-meta-date'] = date
        headers['x-archive-meta-date-string'] = date
        headers['x-archive-meta-date-start'] = '%s-01-01T00:00:00Z' % date


    # e.g 1932-01-29T23:23:59Z
    try:
        dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        headers['x-archive-meta-date'] = str(dt.year)
        headers['x-archive-meta-year'] = str(dt.year)
        headers['x-archive-meta-date-string'] = dt.strftime('%B %-d, %Y')
        headers['x-archive-meta-date-start'] = str(date)
    except:
        pass

    return headers

if __name__ == "__main__":
    main()

