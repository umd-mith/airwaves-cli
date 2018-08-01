import pytest

from airwaves.config import get_config
from airwaves.upload import add_date, get_record, get_headers

def test_timestamp():
    headers = add_date({'Date': '1957-03-03T23:23:59Z'})
    assert headers['x-archive-meta-date'] == '1957'
    assert headers['x-archive-meta-year'] == '1957'
    assert headers['x-archive-meta-date-string'] == 'March 3, 1957'
    assert headers['x-archive-meta-date-start'] == '1957-03-03T23:23:59Z'

def test_year():
    headers = add_date({'Date': '1957'})
    assert headers['x-archive-meta-date'] == '1957'
    assert headers['x-archive-meta-year'] == '1957'
    assert headers['x-archive-meta-date-string'] == '1957'
    assert headers['x-archive-meta-date-start'] == '1957-01-01T00:00:00Z'

def test_year_range():
    headers = add_date({'Date': '1957-1958'})
    assert headers['x-archive-meta-date'] == '1957'
    assert headers['x-archive-meta-year'] == '1957'
    assert headers['x-archive-meta-date-string'] == '1957-1958'
    assert headers['x-archive-meta-date-start'] == '1957-01-01T00:00:00Z'
    assert headers['x-archive-meta-date-end'] == '1958-12-31T23:59:59Z'

def test_get_record():
    id = 'naeb-b110-f04-02'
    config = get_config()

    rec = get_record(
        config['airtable-key'],
        table='Contents by Item with Metadata',
        params={'filterByFormula': '(FIND("%s",{ID}))' % id}
    )
    assert rec['Title'] == 'NAEB Newsletter (February 20, 1931)'

    headers = get_headers(id, 'test.zip', rec, config)
    assert headers['x-archive-meta-title'] == 'NAEB Newsletter (February 20, 1931)'
    assert headers['x-archive-meta-date-string'] == 'February 20, 1931'
    for k, v in headers.items():
        assert type(v) in [unicode, str], '%s was a string or unicode' % k
    

