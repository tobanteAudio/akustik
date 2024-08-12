import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import scipy.signal as signal

from akustik.plot.style import default_styles


def fir_crossover(x, fs=None, fc=None, taps=101):
    # Design a highpass FIR filter by spectral inversion
    lp = signal.firwin(taps, fc, window='hamming', fs=fs)
    hp = -lp
    hp[taps // 2] += 1
    return signal.lfilter(lp, 1.0, x), signal.lfilter(hp, 1.0, x)


def iir_crossover(x: np.ndarray, fs=None, fc=None, order=4):
    lp = signal.butter(order, fc, fs=fs, btype='low', output='sos')
    hp = signal.butter(order, fc, fs=fs, btype='high', output='sos')
    return signal.sosfilt(lp, x), signal.sosfilt(hp, x)


def linkwitz_riley_sos_filter(fc, fs, order=2):
    # Cascading the SOS filters
    # (equivalent to squaring the response of the Butterworth filter)
    lp = signal.butter(order, Wn=fc, fs=fs, btype='low', output='sos')
    hp = signal.butter(order, Wn=fc, fs=fs, btype='high', output='sos')
    return np.concatenate([lp, lp]), np.concatenate([hp, hp])


def linkwitz_riley_crossover(x: np.ndarray, fs=None, fc=None, order=4):
    lp, hp = linkwitz_riley_sos_filter(fc, fs, order=order)
    return signal.sosfilt(lp, x), signal.sosfilt(hp, x)


def report():
    fc = 10
    fs = 96000
    dt = 1/fs
    n = fs

    sig = np.zeros(n, dtype=np.float64)
    sig[0] = 1.0

    lp, hp = fir_crossover(sig, fs, fc, taps=401)
    lp, hp = iir_crossover(sig, fs, fc, order=4)
    lp, hp = linkwitz_riley_crossover(sig, fs, fc, order=4)

    # pad = int(fs/1000*10)
    # lp = np.pad(lp, (pad, 0), "constant", constant_values=0.0)
    # lp = lp[:n-pad]

    freqs = np.fft.rfftfreq(n, d=dt)

    sig_spectrum = np.fft.rfft(sig, n=n)
    sig_amplitude = np.abs(sig_spectrum)
    sig_phase = np.rad2deg(np.angle(sig_spectrum))
    sig_db = 20*np.log10(sig_amplitude+np.spacing(1))

    lp_spectrum = np.fft.rfft(lp, n=n)
    hp_spectrum = np.fft.rfft(hp, n=n)
    mix_spectrum = np.fft.rfft(lp+hp, n=n)

    lp_amplitude = np.abs(lp_spectrum)
    lp_phase = np.rad2deg(np.angle(lp_spectrum))
    lp_db = 20*np.log10(lp_amplitude+np.spacing(1))

    hp_amplitude = np.abs(hp_spectrum)
    hp_phase = np.rad2deg(np.angle(hp_spectrum))
    hp_db = 20*np.log10(hp_amplitude+np.spacing(1))

    mix_amplitude = np.abs(mix_spectrum)
    mix_phase = np.rad2deg(np.angle(mix_spectrum))
    mix_db = 20*np.log10(mix_amplitude+np.spacing(1))

    plt.rcParams.update(default_styles)
    fig, axs = plt.subplots(3, 1)
    fig.suptitle("Crossover")

    # Time
    t = np.linspace(0.0, 1.0, n)
    time: Axes = axs[0]
    time.set_title("Time")
    # time.plot(t, sig, label="Signal")
    time.plot(t, lp, label="LP")
    # time.plot(t, hp, label="HP")
    time.set_xlim((-0.001, 0.5))
    time.legend()

    # Amplitude
    dB: Axes = axs[1]
    dB.set_title("Amplitude")
    dB.semilogx(freqs, mix_db, label="Mix")
    dB.semilogx(freqs, lp_db, label="LP")
    dB.semilogx(freqs, hp_db, label="HP")
    dB.vlines(fc, -100, 0, colors="red", label=f"Crossover {fc} Hz")
    dB.set_ylim((-80, 10))
    dB.set_xlim((1, 40_000))
    dB.grid(which="minor", color='#222222', linestyle=':', linewidth=0.5)
    dB.minorticks_on()
    dB.legend()

    # Phase
    phase: Axes = axs[2]
    phase.set_title("Phase")
    phase.semilogx(freqs, mix_phase, label="Mix")
    # phase.semilogx(freqs, lp_phase, label="LP")
    # phase.semilogx(freqs, hp_phase, label="HP")
    # phase.vlines(fc, np.min(mix_phase), np.max(mix_phase),
    #            colors="red", label=f"Crossover {fc} Hz")
    # phase.set_ylim((-600, -100))
    phase.set_xlim((1, 40_000))
    phase.grid(which="minor", color='#222222', linestyle=':', linewidth=0.5)
    phase.minorticks_on()
    phase.legend()

    plt.show()
