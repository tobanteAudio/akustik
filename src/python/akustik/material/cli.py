import click


@click.group(help="Materials.")
def material():
    pass


@material.command(help="Load excel spreadsheet.")
@click.argument('filename', nargs=1, type=click.Path(exists=True))
def load(filename):
    from akustik.material.load import main
    main(filename)
