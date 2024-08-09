import click


@click.group(help="Wave equation simulations.")
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
@click.option('--engine_exe', type=click.Path(exists=True, executable=True))
@click.option('--duration', type=float, default=0.1)
@click.option('--fmax', type=float)
@click.option('--ppw', type=float, default=10.5)
@click.option('--save', is_flag=True, help='Save output to data-dir.')
@click.option('--sim_dir', type=click.Path())
@click.option('--video', is_flag=True, help='Save video to data-dir.')
@click.pass_context
def sim2d(ctx, c, duration, engine_exe, fmax, ppw, save, sim_dir, video):
    from akustik.wave.sim2d import main
    main(
        apply_loss=True,
        apply_rigid=True,
        c=c,
        duration=duration,
        engine_exe=engine_exe,
        fmax=fmax,
        ppw=ppw,
        save=save,
        sim_dir=sim_dir,
        verbose=ctx.obj['VERBOSE'],
        video=video
    )
