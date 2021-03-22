import click

import logging
import airwaves.aapb
import airwaves.upload

logging.basicConfig(filename='airwaves.log', level=logging.INFO)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('id')
@click.argument('zip_file')
def upload(id, zip_file):
    airwaves.upload.main(id, zip_file)

@cli.command()
def items():
    for record in airwaves.aapb.records():
        print("{} {}".format(record['id'], record['title']))

@cli.command()
@click.argument('id')
def transcript(id):
    t = aapb.get_transcript(id)
    print(t)

@cli.command()
def transcripts():
    for record in aapb.records():
        t = aapb.get_transcript(record['id'])
        has_transcript = 'code' not in t
        print('%s [%s]' % (record['id'], '+' if has_transcript else '-'))
