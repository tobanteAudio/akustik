import click


@click.group(help="Diffusors.")
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
