import numpy as np

from akustik.diffusor.design import diffusor_bandwidth, diffusor_dimensions
from akustik.diffusor.prd import primitive_root_diffuser as prd
from akustik.diffusor.qrd import quadratic_residue_diffuser as qrd


def test_diffusor_bandwidth():
    fmin, fmax = diffusor_bandwidth(0.01, 0.1)
    assert np.allclose(fmin, 857.5)
    assert np.allclose(fmax, 17150.0)

    fmin, fmax = diffusor_bandwidth(0.02, 0.1)
    assert np.allclose(fmin, 857.5)
    assert np.allclose(fmax, 8575.0)

    fmin, fmax = diffusor_bandwidth(0.01, 0.2)
    assert np.allclose(fmin, 428.75)
    assert np.allclose(fmax, 17150.0)


def test_diffusor_dimensions():
    well_width, max_depth = diffusor_dimensions(857.5, 17150.0)
    assert np.allclose(well_width, 0.01)
    assert np.allclose(max_depth, 0.1)

    well_width, max_depth = diffusor_dimensions(857.5,  8575.0)
    assert np.allclose(well_width, 0.02)
    assert np.allclose(max_depth, 0.1)

    well_width, max_depth = diffusor_dimensions(428.75, 17150.0)
    assert np.allclose(well_width, 0.01)
    assert np.allclose(max_depth, 0.2)


def test_quadratic_residue_diffuser():
    assert np.allclose(qrd(5, depth=None), [0, 1, 4, 4, 1])
    assert np.allclose(qrd(7, depth=None), [0, 1, 4, 2, 2, 4, 1])
    assert np.allclose(qrd(11, depth=None), [0, 1, 4, 9, 5, 3, 3, 5, 9, 4, 1])

    assert np.allclose(qrd(5, depth=10), [0, 2.5, 10, 10, 2.5])
    assert np.allclose(qrd(11), [0, 1, 4, 9, 5, 3, 3, 5, 9, 4, 1])


def test_primitive_root_diffuser():
    n, g = prd(5)
    assert g == 2
    assert np.allclose(n, [1, 2, 4, 3])

    n, g = prd(5, depth=0.1)
    assert g == 2
    assert np.allclose(n, [0.025, 0.05, 0.1, 0.075])

    n, g = prd(5, g=2)
    assert g == 2
    assert np.allclose(n, [1, 2, 4, 3])

    n, g = prd(7)
    assert g == 3
    assert np.allclose(n, [1, 3, 2, 6, 4, 5])

    n, g = prd(11)
    assert g == 2
    assert np.allclose(n, [1, 2, 4, 8, 5, 10, 9, 7, 3, 6])
