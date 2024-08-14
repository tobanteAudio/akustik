import numpy as np

from akustik.loudness import sound_attenuation


def test_sound_attenuation():
    SPL_1 = 100
    R_1 = 1
    assert np.allclose(sound_attenuation(SPL_1, R_1, 1), 100)
    assert np.allclose(sound_attenuation(SPL_1, R_1, 2), 93.9794)
    assert np.allclose(sound_attenuation(SPL_1, R_1, 3), 90.4575)
    assert np.allclose(sound_attenuation(SPL_1, R_1, 4), 87.9588)
