import numpy as np
import pytest

from akustik.speaker.thiele_small import (
    effective_moving_mass,
    resonance_frequency,
    total_q_factor,
)


@pytest.mark.parametrize("fs, Cms,  Mms", [
    (29.0, 0.000253, 0.119048),
    (26.0, 0.000160, 0.234192),
])
def test_effective_moving_mass(fs, Cms, Mms):
    assert np.allclose(effective_moving_mass(fs=fs, Cms=Cms), Mms)


@pytest.mark.parametrize("Cms, Mms, fs", [
    (0.000171, 0.319, 21.548980),
    (0.000143, 0.499, 18.840908),
])
def test_resonance_frequency(Cms, Mms, fs):
    assert np.allclose(resonance_frequency(Cms=Cms, Mms=Mms), fs)


@pytest.mark.parametrize("Qms, Qes, Qts", [
    (3.69, 0.346, 0.316337),
    (4.05, 0.347, 0.319615),
])
def test_total_q_factor(Qms, Qes, Qts):
    assert np.allclose(total_q_factor(Qms=Qms, Qes=Qes), Qts)
