def diffusor_bandwidth(well_width, max_depth, c=343.0):
    # fmax calculation matches multiple online calculators.
    # Not sure about fmin.
    fmin = c/(max_depth*4)
    fmax = c/(well_width*2)
    return fmin, fmax


def diffusor_dimensions(fmin, fmax, c=343.0):
    # fmax calculation matches multiple online calculators.
    # Not sure about fmin.
    well_width = c/(fmax*2)
    max_depth = c/(fmin*4)
    return well_width, max_depth
