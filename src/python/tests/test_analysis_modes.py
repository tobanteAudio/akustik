import numpy as np

from akustik.analysis.modes import frequency_spacing_index, room_mode, room_mode_kind


def test_frequency_spacing_index():
    # Matches table in paper:
    # Preferred dimension ratios of small rectangular rooms, Jens Holger Rindel, 2021

    # Ratio-B
    L = 7.0
    W = 5.19
    H = 3.72
    S = 0.9
    assert np.allclose(frequency_spacing_index(L, W, H), 1.51521)
    assert np.allclose(frequency_spacing_index(L*S, W*S, H*S), 1.51521)

    # Cube
    L = 5
    W = 5
    H = 5
    assert np.allclose(frequency_spacing_index(L, W, H), 3.71218)
    assert np.allclose(frequency_spacing_index(L*S, W*S, H*S), 3.71218)

    # Double Cube
    L = 10
    W = 5
    H = 5
    assert np.allclose(frequency_spacing_index(L, W, H), 3.90988)
    assert np.allclose(frequency_spacing_index(L*S, W*S, H*S), 3.90988)


def test_room_mode():
    L = 8.0
    W = 6.0
    H = 4.0

    assert np.allclose(room_mode(L, W, H, 1, 0, 0), 21.4375)
    assert np.allclose(room_mode(L, W, H, 0, 1, 0), 28.5833)
    assert np.allclose(room_mode(L, W, H, 0, 0, 1), 42.8750)

    assert np.allclose(room_mode(L, W, H, 1, 0, 1), 47.9357)
    assert np.allclose(room_mode(L, W, H, 1, 1, 1), 55.8107)


def test_room_mode_kind():
    for i in range(1, 10):
        assert room_mode_kind(i, 0, 0) == "axial"
        assert room_mode_kind(0, i, 0) == "axial"
        assert room_mode_kind(0, 0, i) == "axial"

        assert room_mode_kind(i, i, 0) == "tangential"
        assert room_mode_kind(0, i, i) == "tangential"
        assert room_mode_kind(i, 0, i) == "tangential"

        assert room_mode_kind(i, i, i) == "oblique"
