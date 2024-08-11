import click


@click.group(help="Loudspeakers.")
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


@speaker.command(help="Dayton Audio Test System.")
@click.pass_context
@click.option('--fmin', default=10, show_default=True)
@click.option('--fmax', default=30000, show_default=True)
@click.argument('dats_dirs', nargs=-1, type=click.Path(exists=True))
def dats(ctx, dats_dirs, fmin, fmax):
    from akustik.speaker.dats import report
    report(dats_dirs, fmin, fmax)


@speaker.command(help="Power requirements.")
@click.pass_context
@click.option('--driver_db', type=click.Path(exists=True))
@click.option('--spl_target', default=108, show_default=True)
def power(ctx, spl_target, driver_db):
    from akustik.speaker.power import report
    report(driver_db, spl_target)


@speaker.command(help="Thiele/Small parameters.")
@click.option('--driver_db', type=click.Path(exists=True))
@click.argument('drivers', nargs=-1, type=str)
@click.pass_context
def ts(ctx, driver_db, drivers):
    from akustik.speaker.thiele_small import report
    report(driver_db, list(drivers))
