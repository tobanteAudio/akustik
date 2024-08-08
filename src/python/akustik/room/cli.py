import click

import akustik.room.decay as decay


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
@click.option('--fmax', type=float, default=1000.0)
@click.option('--fmin', type=float, default=20.0)
@click.option('--sim_dir', type=click.Path(exists=True))
@click.option('--target', type=float, default=0.3)
@click.argument('filenames', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def rt60(ctx, filenames, fmax, fmin, sim_dir, target):
    decay.report(
        filenames=filenames,
        fmin=fmin,
        fmax=fmax,
        show_tolerance=True,
        show_all=True,
        sim_dir=sim_dir,
        target=target
    )
