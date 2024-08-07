import numpy as np

from akustik.room.decay import rt60_target


def test_rt60_target():
    assert np.allclose(rt60_target(50.0), 0.2)
    assert np.allclose(rt60_target(100.0), 0.25)
    assert np.allclose(rt60_target(200.0), 0.31498)
    assert np.allclose(rt60_target(400.0), 0.39685)
    assert np.allclose(rt60_target(450.0), 0.4)
