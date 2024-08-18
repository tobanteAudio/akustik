import numpy as np

from akustik.speaker.dats import (
    max_impedance,
    read_dats_folder,
)


def test_max_sound_pressure():
    folder = "src/python/tests/data/dats/RSS390HF-4"
    name, frd, zma = read_dats_folder(folder)
    assert name == "RSS390HF-4"
    assert frd.shape == (416, 3)
    assert zma.shape == (344, 3)

    Z: np.ndarray = zma["Impedance"].to_numpy()
    f: np.ndarray = zma["Frequency"].to_numpy()
    assert np.allclose(max_impedance(Z, f), (21.173, 19.585))
