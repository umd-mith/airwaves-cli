import click

import airwaves.upload

@click.group()
def cli():
    pass

@cli.command()
@click.argument('id')
@click.argument('zip_file')
def upload(id, zip_file):
    airwaves.upload.main(id, zip_file)
