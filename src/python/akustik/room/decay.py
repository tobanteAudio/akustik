import glob
import os
import pathlib

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter
import numpy as np
from scipy.io import wavfile

from akustik.frequency.octave import iso_third_octave_bands, third_octave_filter
from akustik.plot.style import default_styles


def _collect_wav_files(directory, pattern="*.wav"):
    search_pattern = os.path.join(directory, pattern)
    wav_files = glob.glob(search_pattern)
    return wav_files


def _calculate_t60(edc_db, fs):
    t = np.arange(len(edc_db)) / fs
    edc_db -= np.max(edc_db)  # Normalize to 0 dB at the start
    start_idx = np.where(edc_db <= -5)[0][0]
    end_idx = np.where(edc_db <= -35)[0][0]
    t60 = 2 * (t[end_idx] - t[start_idx])
    return t60


def energy_decay_curve(ir):
    edc = np.cumsum(ir[::-1]**2)[::-1]
    edc_db = 10 * np.log10(edc / np.max(edc))
    return edc_db


def rt60_target(volume) -> float:
    """Formula given in section 2.3 of 'EBU Tech. 3276'
    """
    T60_min = 0.2
    T60_max = 0.4
    V0 = 100
    return max(T60_min, min(T60_max, 0.25*(volume/V0)**(1/3)))


def decay_times_for_bands(files, centre_frequencies):
    file_times = []
    file_names = []
    for path in files:
        file = pathlib.Path(path).absolute()
        fs, ir = wavfile.read(file)
        t60_times = []
        print(f"---- {file.stem} ----")
        for fc in centre_frequencies:
            edc_db = energy_decay_curve(third_octave_filter(ir, fs, fc))
            t60 = _calculate_t60(edc_db, fs)
            t60_times.append(round(t60, 3))
            print(f"T60 at {fc} Hz: {t60:.2f} seconds")

        file_times.append(np.array(t60_times))
        file_names.append(file.stem[:4])
    return file_times, file_names


def third_octave_bands(fmin, fmax):
    bands = iso_third_octave_bands()
    bands = bands[np.where(bands >= fmin)]
    bands = bands[np.where(bands <= fmax)]
    return bands


def plot_decay_times(
    file_times=None,
    file_names=None,
    fmin=None,
    fmax=None,
    center_freqs=None,
    show_all=True,
    show_tolerance=True,
    target=None
):
    plt.rcParams.update(default_styles)

    _, axs = plt.subplots(2, 1)
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

        ax.set_title("Tolerance")
        ax.set_ylabel("Difference [s]")
        ax.set_xlabel("Frequency [Hz]")
        ax.xaxis.set_major_formatter(formatter)

        ax.set_xlim((fmin, fmax))
        ax.set_ylim((ymin-0.05, ymax+0.05))

        ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.5)
        ax.minorticks_on()
        ax.legend(loc='upper right')

    plt.show()


def main(filenames, fmin, fmax, show_all=False, show_tolerance=True, sim_dir=None, target=None):
    center_freqs = third_octave_bands(fmin, fmax)

    if sim_dir and len(filenames) > 0:
        raise RuntimeError("--sim_dir not valid, when comparing IRs")

    files = filenames
    if sim_dir:
        files = _collect_wav_files(sim_dir, "*_out_normalised.wav")
    files = list(sorted(list(files)))
    file_times, file_names = decay_times_for_bands(files, center_freqs)

    plot_decay_times(file_times, file_names, fmin, fmax,
                     center_freqs, show_all, show_tolerance, target)
