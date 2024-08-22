import click


@click.group(help="Absorber.")
def absorber():
    pass


@absorber.command(help="TubeTrap.")
def tubetrap():
    from akustik.absorber.tubetrap import main
    main()
