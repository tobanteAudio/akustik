import click


@click.group(help="Rooms.")
def room():
    pass


@room.command(help="Room modes.")
def modes():
    pass


@room.command(help="Reverberation time.")
@click.option('--fmax', type=float, default=1000.0)
@click.option('--fmin', type=float, default=20.0)
@click.option('--sim_dir', type=click.Path(exists=True))
@click.option('--target', type=float, default=0.3)
@click.argument('filenames', nargs=-1, type=click.Path(exists=True))
def rt60(filenames, fmax, fmin, sim_dir, target):
    from akustik.room.decay import main
    main(
        filenames=filenames,
        fmin=fmin,
        fmax=fmax,
        show_tolerance=True,
        show_all=True,
        sim_dir=sim_dir,
        target=target
    )
