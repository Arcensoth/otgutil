import logging

import click

from otgutil import structure

log = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@click.command()
@click.argument('structure_file')
@click.argument('output_file')
def convert(structure_file, output_file):
    try:
        structure.structure_file_to_bo3_blocks(structure_file, output_file)
        click.echo('Successfully converted structure')
    except:
        msg = 'Failed to convert structure'
        click.echo(msg)
        log.exception(msg)


cli.add_command(convert)

cli()
