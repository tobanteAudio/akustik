import numpy as np

from akustik.speaker.thiele_small import (
    resonance_frequency,
    total_q_factor,
)


def test_resonance_frequency():
    assert np.allclose(resonance_frequency(Cms=0.000171, Mms=0.319), 21.548980)
    assert np.allclose(resonance_frequency(Cms=0.000143, Mms=0.499), 18.840908)


def test_total_q_factor():
    assert np.allclose(total_q_factor(Qms=3.69, Qes=0.346), 0.316337)
    assert np.allclose(total_q_factor(Qms=4.05, Qes=0.347), 0.319615)
