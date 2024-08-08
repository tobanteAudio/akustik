import click

from akustik.diffusor.cli import diffusor
from akustik.room.cli import room
from akustik.speaker.cli import speaker
from akustik.wave.cli import wave


@click.group()
@click.option('--verbose', is_flag=True, help='Print debug output.')
@click.pass_context
def main(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


main.add_command(diffusor)
main.add_command(room)
main.add_command(speaker)
main.add_command(wave)
