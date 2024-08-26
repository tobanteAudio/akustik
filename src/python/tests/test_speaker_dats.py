import numpy as np

from akustik.speaker.dats import (
    find_f1_f2,
    max_impedance,
    read_dats_folder,
)


def test_find_f1_f2():
    folder = "src/python/tests/data/dats/RSS390HF-4"
    name, frd, zma = read_dats_folder(folder)
    assert name == "RSS390HF-4"
    assert frd.shape == (416, 3)
    assert zma.shape == (344, 3)

    Re = 3.0
    Z: np.ndarray = zma["Impedance"].to_numpy()
    f: np.ndarray = zma["Frequency"].to_numpy()
    assert np.allclose(max_impedance(Z, f), (21.173, 19.585))
    assert np.allclose(find_f1_f2(Re, Z, f), (13.454, 30.204))
