import click


@click.group()
@click.option('--verbose', is_flag=True, help='Print debug output.')
@click.pass_context
def main(ctx, verbose):
    # ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


@main.group(help="Diffusors.")
@click.pass_context
def diffusor(ctx):
    pass


@diffusor.command(help="Diffusor design.")
@click.pass_context
def design(ctx):
    from akustik.diffusor.design import main
    main()


@diffusor.command(help="Primitive root diffuser.")
@click.pass_context
def prd(ctx):
    from akustik.diffusor.prd import main
    main()


@diffusor.command(help="Quadratic residue diffuser.")
@click.pass_context
def qrd(ctx):
    from akustik.diffusor.qrd import main
    main()


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


@main.group(help="Wave equation simulations.")
@click.pass_context
def wave(ctx):
    pass


@wave.command(help="2D wave-equation report.")
@click.option('--sim_dir', type=click.Path(exists=True))
@click.pass_context
def report2d(ctx, sim_dir):
    from akustik.wave.report2d import main
    main(sim_dir)


@wave.command(help="2D wave-equation simulation.")
@click.option('--c', type=float, default=343.0)
@click.option('--sim_dir', type=click.Path())
@click.option('--duration', type=float, default=0.1)
@click.option('--fmax', type=float)
@click.option('--ppw', type=float, default=10.5)
@click.option('--save', is_flag=True, help='Save output to data-dir.')
@click.option('--video', is_flag=True, help='Save video to data-dir.')
@click.pass_context
def sim2d(ctx, c, sim_dir, duration, fmax, ppw, save, video):
    from akustik.wave.sim2d import main
    main(
        apply_loss=True,
        apply_rigid=True,
        c=c,
        duration=duration,
        fmax=fmax,
        ppw=ppw,
        save=save,
        sim_dir=sim_dir,
        verbose=ctx.obj['VERBOSE'],
        video=video
    )
