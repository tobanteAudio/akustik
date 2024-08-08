import click


@click.group(help="Rooms.")
@click.pass_context
def room(ctx):
    pass


@room.command(help="Room modes.")
@click.pass_context
def modes(ctx):
    if ctx.obj['VERBOSE']:
        click.echo('Modes')


@room.command(help="Reverberation time.")
@click.pass_context
def rt60(ctx):
    if ctx.obj['VERBOSE']:
        click.echo('RT60')
