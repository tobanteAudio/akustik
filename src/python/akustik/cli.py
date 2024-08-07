import click


@click.group()
@click.option('--verbose', is_flag=True, help='Print debug output.')
@click.pass_context
def main(ctx, verbose):
    # ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


@main.command(help="Room modes")
@click.pass_context
def modes(ctx):
    if ctx.obj['VERBOSE']:
        click.echo('Modes')


@main.command(help="Reverberation time")
@click.pass_context
def rt60(ctx):
    if ctx.obj['VERBOSE']:
        click.echo('RT60')


@main.command(help="Loudspeakers")
@click.pass_context
def speaker(ctx):
    if ctx.obj['VERBOSE']:
        click.echo('Speaker')
