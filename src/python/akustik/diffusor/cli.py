import click


@click.group(help="Diffusors.")
def diffusor():
    pass


@diffusor.command(help="Primitive root diffuser.")
def prd():
    from akustik.diffusor.prd import main
    main()


@diffusor.command(help="Quadratic residue diffuser.")
def qrd():
    from akustik.diffusor.qrd import main
    main()
