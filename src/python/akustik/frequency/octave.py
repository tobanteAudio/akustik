import numpy as np
from scipy import signal


def iso_third_octave_bands(min_idx: int = 0, max_idx: int = 43):
    assert max_idx >= min_idx

    frequencies = []
    for idx in range(min_idx, max_idx+1):
        frequencies.append(10**(0.1*idx))
    return np.array(frequencies)


def third_octave_filter(sig, fs, center):
    factor = 2 ** (1/6)  # One-third octave factor
    low = center / factor
    high = center * factor
    sos = signal.butter(4, [low, high], btype='band', fs=fs, output='sos')
    return signal.sosfilt(sos, sig)
