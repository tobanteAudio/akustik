import click


@click.group()
@click.option('--verbose', is_flag=True, help='Print debug output.')
@click.pass_context
def main(ctx, verbose):
    # ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


@main.group(help="Rooms.")
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


@main.group(help="Loudspeakers.")
@click.pass_context
def speaker(ctx):
    pass


@speaker.command(help="Driver alignment.")
@click.pass_context
def alignment(ctx):
    from akustik.speaker.alignment import report
    report()


@speaker.command(help="Crossover design.")
@click.pass_context
def crossover(ctx):
    from akustik.speaker.crossover import report
    report()


@speaker.command(help="Power requirements.")
@click.pass_context
@click.option('--driver_db', type=click.Path(exists=True))
@click.option('--spl_target', default=108, show_default=True)
def power(ctx, spl_target, driver_db):
    from akustik.speaker.power import report
    report(driver_db, spl_target)
