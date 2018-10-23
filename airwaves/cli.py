import click

import aapb
import airwaves.upload

@click.group()
def cli():
    pass

@cli.command()
@click.argument('id')
@click.argument('zip_file')
def upload(id, zip_file):
    airwaves.upload.main(id, zip_file)

@cli.command()
def ids():
    for record in aapb.records():
        print(record['id'], record['title'])

@cli.command()
@click.argument('id')
def transcript(id):
    t = aapb.get_transcript(id)
    print(t)
