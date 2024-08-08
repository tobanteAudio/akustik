import glob
import os
import pathlib

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal

from akustik.plot.style import default_styles


def _collect_wav_files(directory, pattern="*.wav"):
    search_pattern = os.path.join(directory, pattern)
    wav_files = glob.glob(search_pattern)
    return wav_files


def _third_octave_filter(sig, fs, center):
    factor = 2 ** (1/6)  # One-third octave factor
    low = center / factor
    high = center * factor
    sos = signal.butter(4, [low, high], btype='band', fs=fs, output='sos')
    return signal.sosfilt(sos, sig)


def _energy_decay_curve(ir):
    edc = np.cumsum(ir[::-1]**2)[::-1]
    edc_db = 10 * np.log10(edc / np.max(edc))
    return edc_db


def _calculate_t60(edc_db, fs):
    t = np.arange(len(edc_db)) / fs
    edc_db -= np.max(edc_db)  # Normalize to 0 dB at the start
    start_idx = np.where(edc_db <= -5)[0][0]
    end_idx = np.where(edc_db <= -35)[0][0]
    t60 = 2 * (t[end_idx] - t[start_idx])
    return t60


def rt60_target(volume) -> float:
    """Formula given in section 2.3 of 'EBU Tech. 3276'
    """
    T60_min = 0.2
    T60_max = 0.4
    V0 = 100
    return max(T60_min, min(T60_max, 0.25*(volume/V0)**(1/3)))


def report(filenames, fmin, fmax, show_all=False, show_tolerance=True, sim_dir=None, target=None):
    if sim_dir and len(filenames) > 0:
        raise RuntimeError("--sim_dir not valid, when comparing IRs")

    files = filenames
    if sim_dir:
        files = _collect_wav_files(sim_dir, "*_out_normalised.wav")

    files = list(sorted(list(files)))

    # ISO 1/3 octaves
    center_freqs = np.array([
        20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160,
        200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
        2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000,
        20000
    ])

    center_freqs = center_freqs[np.where(center_freqs >= fmin)]
    center_freqs = center_freqs[np.where(center_freqs <= fmax)]

    file_times = []
    file_names = []
    for path in files:
        file = pathlib.Path(path).absolute()
        fs, ir = wavfile.read(file)
        t60_times = []
        print(f"---- {file.stem} ----")
        for center_freq in center_freqs:
            filtered_ir = _third_octave_filter(ir, fs, center_freq)
            edc_db = _energy_decay_curve(filtered_ir)
            t60 = _calculate_t60(edc_db, fs)
            t60_times.append(round(t60, 3))
            print(f"T60 at {center_freq} Hz: {t60:.2f} seconds")

        file_times.append(np.array(t60_times))
        file_names.append(file.stem[:4])

    plt.rcParams.update(default_styles)

    fig, axs = plt.subplots(2, 1)
    formatter = ScalarFormatter()
    formatter.set_scientific(False)

    # T60
    ax: Axes = axs[0]
    ax.margins(0, 0.1)

    if show_all:
        for f, name in zip(file_times, file_names):
            ax.semilogx(center_freqs, f, label=f"{name}")
    else:
        ax.semilogx(center_freqs, file_times[0], label="Measurement")

    if target:
        ax.hlines(
            target,
            fmin,
            fmax,
            color='#555555',
            label=f"Target {target} s",
            linestyles="dashed",
        )

    ax.set_title("RT60")
    ax.set_ylabel("Decay [s]")
    ax.set_xlabel("Frequency [Hz]")
    ax.xaxis.set_major_formatter(formatter)

    ax.set_xlim((fmin, fmax))
    ax.set_ylim((0.0, np.max(file_times)+0.1))

    ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.5)
    ax.minorticks_on()
    ax.legend(loc='upper right')

    # Tolerance
    if show_tolerance:
        k4 = min(fmax, 4000)
        k8 = min(fmax, 8000)
        k20 = min(fmax, 20000)

        ax: Axes = axs[1]
        ax.margins(0, 0.1)
        ymin, ymax = -0.05, +0.3
        if show_all:
            for f, name in zip(file_times, file_names):
                diff = np.insert(np.diff(f), 0, 0.0)
                diff = np.insert(f[:-1]-f[1:], 0, 0.0)
                ax.semilogx(center_freqs, diff, label=f"{name}")
                ymin, ymax = min(ymin, np.min(diff)), max(ymax, np.max(diff))
        else:
            diff = np.insert(np.diff(file_times[0]), 0, 0.0)
            diff = np.insert(file_times[0][:-1]-file_times[0][1:], 0, 0.0)
            ax.semilogx(center_freqs, diff, label="Measurement")
            ymin, ymax = np.min(diff), np.max(diff)

        ax.plot([63.0, 200.0], [0.3, 0.05], color='#555555')
        ax.hlines(
            [+0.05, -0.05, -0.1, -0.1, +0.3, +0.05, -0.05],
            [200, 100, k4,  k8, fmin, k8, fmin],
            [k8, k4, k8,  k20, 63, k20, 100],
            linestyles=["-", "-", "-", "--", "--", "--", "--"],
            colors='#555555',
            label="EBU Tech 3000"
        )

        ax.set_title(f"Tolerance")
        ax.set_ylabel("Difference [s]")
        ax.set_xlabel("Frequency [Hz]")
        ax.xaxis.set_major_formatter(formatter)

        ax.set_xlim((fmin, fmax))
        ax.set_ylim((ymin-0.05, ymax+0.05))

        ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.5)
        ax.minorticks_on()
        ax.legend(loc='upper right')

    plt.show()
