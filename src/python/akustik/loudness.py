import numpy as np


def sound_attenuation(SPL_1, R_1, R_2):
    """
    Sound attenuation with increasing distance from the sound source.

    SPL_1: Sound pressure level at point 1
    R_1: Distance from the sound source to point 1
    R_2: Distance from the sound source to point 2
    """
    return SPL_1 - 20*np.log10(R_2/R_1)
