import numpy as np

from akustik.frequency.octave import iso_third_octave_bands


def test_iso_third_octave_bands():
    bands = iso_third_octave_bands()
    assert bands.shape == (44,)
    assert np.allclose(bands[0], 1.0)
    assert np.allclose(bands[10], 10.0)
    assert np.allclose(bands[20], 100.0)
    assert np.allclose(bands[30], 1000.0)
    assert np.allclose(bands[43], 19952.623149)

    bands = iso_third_octave_bands(10, 40)
    assert bands.shape == (31,)
    assert np.allclose(bands[0], 10.0)
    assert np.allclose(bands[10], 100.0)
    assert np.allclose(bands[20], 1000.0)
