import click


@click.group(help="Loudspeakers.")
def speaker():
    pass


@speaker.command(help="Driver alignment.")
def alignment():
    from akustik.speaker.alignment import main
    main()


@speaker.command(help="Crossover design.")
def crossover():
    from akustik.speaker.crossover import main
    main()


@speaker.command(help="Dayton Audio Test System.")
@click.option('--fmin', default=10, show_default=True)
@click.option('--fmax', default=30000, show_default=True)
@click.option('--re', type=float, help="DC Resistance")
@click.argument('dats_dirs', nargs=-1, type=click.Path(exists=True))
def dats(dats_dirs, fmin, fmax, re):
    from akustik.speaker.dats import main
    main(dats_dirs, fmin, fmax, Re=re)


@speaker.command(help="Power requirements.")
@click.option('--driver_db', type=click.Path(exists=True))
@click.option('--spl_target', default=108, show_default=True)
def power(spl_target, driver_db):
    from akustik.speaker.power import main
    main(driver_db, spl_target)


@speaker.command(help="Thiele/Small parameters.")
@click.option('--driver_db', type=click.Path(exists=True))
@click.argument('drivers', nargs=-1, type=str)
def ts(driver_db, drivers):
    from akustik.speaker.thiele_small import main
    main(driver_db, list(drivers))
