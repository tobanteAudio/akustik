import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, firwin, lfilter


def report():
    fc = 400
    fs = 96000
    dt = 1/fs
    n = fs

    sig = np.zeros(n, dtype=np.float64)
    sig[0] = 1.0

    num_taps = 101
    lowpass_taps = firwin(num_taps, fc, window='hamming', fs=fs)

    # Design a highpass FIR filter by spectral inversion
    highpass_taps = -lowpass_taps
    highpass_taps[num_taps // 2] += 1

    lowpass_sig = lfilter(lowpass_taps, 1.0, sig)
    highpass_sig = lfilter(highpass_taps, 1.0, sig)

    freqs = np.fft.rfftfreq(n, d=dt)
    lowpass_spectrum = np.fft.rfft(lowpass_sig)
    highpass_spectrum = np.fft.rfft(highpass_sig)

    lowpass_amplitude = np.abs(lowpass_spectrum)
    highpass_amplitude = np.abs(highpass_spectrum)
    lowpass_phase = np.angle(lowpass_spectrum)
    highpass_phase = np.angle(highpass_spectrum)
    mix_amplitude = lowpass_amplitude+highpass_amplitude
    mix_phase = lowpass_phase+highpass_phase
    mix_db = 20*np.log10(mix_amplitude)

    # plt.semilogx(freqs, 20*np.log10(lowpass_amplitude), label="LP")
    # plt.semilogx(freqs, 20*np.log10(highpass_amplitude), label="HP")
    # plt.vlines(fc, -100, 0, colors="red")
    plt.semilogx(freqs, lowpass_phase, label="LP")
    plt.semilogx(freqs, highpass_phase+0.1, label="HP")
    # plt.semilogx(freqs, mix_phase, label="LP+HP")
    # plt.vlines(fc, np.min(mix_db), np.max(mix_db), colors="red")
    plt.xlim((10, 40_000))
    # plt.ylim((-100, 0))
    plt.grid()
    plt.legend()
    plt.show()
