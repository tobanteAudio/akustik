import numpy as np

from akustik.speaker.power import max_sound_pressure


def test_max_sound_pressure():
    assert np.allclose(max_sound_pressure(85, 1, 1), 85)
    assert np.allclose(max_sound_pressure(90, 1, 1), 90)

    assert np.allclose(max_sound_pressure(90, 2, 1), 93.0102)
