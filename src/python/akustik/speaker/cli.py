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


@speaker.command(help="Power requirements.")
@click.pass_context
@click.option('--driver_db', type=click.Path(exists=True))
@click.option('--spl_target', default=108, show_default=True)
def power(ctx, spl_target, driver_db):
    from akustik.speaker.power import report
    report(driver_db, spl_target)
