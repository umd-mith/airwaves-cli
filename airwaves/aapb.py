import requests

from airwaves.config import get_config

config = get_config()

def records():
    params = {
        'q': 'special_collection:naeb',
        'sort': 'year asc',
        'rows': 20,
        'start': 0
    }
    while True:
        found = False
        resp = requests.get('http://americanarchive.org/api.json', params)
        if resp.status_code == 200:
            for rec in resp.json()['response']['docs']:
                found = True
                yield rec
            if found:
                params['start'] += 20
                import time; time.sleep(0.5)
            else:
                break

def get_transcript(id):
    resp = requests.get(
        'http://americanarchive.org/api/{}/transcript'.format(id),
        auth=(config['aapb-username'], config['aapb-password'])
    )
    return resp.json()
