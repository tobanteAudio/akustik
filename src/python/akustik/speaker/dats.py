import glob
import pathlib

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter
import numpy as np
from scipy.interpolate import interp1d

from akustik.plot.style import default_styles


def _axes_style(ax: Axes, fmin, fmax):
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_xlabel('Frequency [Hz]')
    ax.set_xlim((fmin, fmax))
    ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.5)
    ax.minorticks_on()
    ax.legend()

    return ax


def max_impedance(Z: np.ndarray, f: np.ndarray):
    fmax = np.max(f)
    Z = Z[f < fmax/4]
    Zmax_index = np.argmax(Z)
    return Z[Zmax_index], f[Zmax_index]


def read_dats_frequency_response(path):
    return pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["Frequency", "SPL", "Phase"]
    )


def read_dats_impedance_response(path):
    return pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["Frequency", "Impedance", "Phase"]
    )


def read_dats_folder(folder):
    folder = pathlib.Path(folder)
    frd_files = glob.glob(str(folder/"FRD"/"*.frd"))
    zma_files = glob.glob(str(folder/"ZMA"/"*.zma"))

    name = pathlib.Path(zma_files[0]).stem
    frd = read_dats_frequency_response(frd_files[0])
    zma = read_dats_impedance_response(zma_files[0])
    return name, frd, zma


def find_f1_f2(Re, Z: np.ndarray, f: np.ndarray):
    assert f.shape == Z.shape
    Zmax, freq = max_impedance(Z, f)
    Z12 = np.sqrt(Re*Zmax)

    Z_f1 = Z[f < freq]
    f_f1 = f[f < freq]
    Z1_index = np.abs(Z_f1 - Z12).argmin()
    Z1 = Z_f1[Z1_index]
    f1 = f_f1[Z1_index]

    Z = Z[(f > freq) & (f < freq*2)]
    f = f[(f > freq) & (f < freq*2)]
    Z2_index = np.abs(Z - Z12).argmin()
    Z2 = Z[Z2_index]
    f2 = f[Z2_index]

    print(f"{freq=}")
    print(f"{Zmax=}")
    print(f"{Z12=}")
    print(f"{Z1=}")
    print(f"{f1=}")
    print(f"{Z2=}")
    print(f"{f2=}")

    return f1, f2


def main(dats_dirs, fmin, fmax, Re=None, plot=True):
    data = {
        "name": [],
        "acoustic": {
            "freq": [],
            "spl": [],
            "phase": [],
        },
        "electric": {
            "freq": [],
            "impedance": [],
            "phase": [],
        },
    }

    for folder in dats_dirs:
        name, frd, zma = read_dats_folder(folder)

        if Re is not None:
            f: np.ndarray = zma["Frequency"].to_numpy()
            phase: np.ndarray = zma["Phase"].to_numpy()
            Z: np.ndarray = zma["Impedance"].to_numpy()

            # freq = np.insert(freq, 0, 0.0)
            # spl = np.insert(spl, 0, 0.0)
            # assert freq.shape == spl.shape

            # freq_new = np.fft.rfftfreq(4096*64, 1/(np.max(freq)*2))
            # interpolator = interp1d(freq, spl, kind='cubic')
            # spl_new = interpolator(freq_new)
            # print(freq_new)
            # print(spl_new)

            Z = np.insert(Z, 0, 0.0)
            f = np.insert(f, 0, 0.0)
            phase = np.insert(phase, 0, 0.0)

            f_new = np.linspace(np.min(f), np.max(f), 1024*512)
            Z_new = interp1d(f, Z, kind='cubic')(f_new)
            phase_new = interp1d(f, phase, kind='cubic')(f_new)

            find_f1_f2(Re, Z, f)
            print("---")
            find_f1_f2(Re, Z_new, f_new)

        if plot:
            data["name"].append(name)
            data["acoustic"]["freq"].append(frd["Frequency"].to_numpy())
            data["acoustic"]["spl"].append(frd["SPL"].to_numpy())
            data["acoustic"]["phase"].append(frd["Phase"].to_numpy())
            data["electric"]["freq"].append(f_new)
            data["electric"]["phase"].append(phase_new)
            data["electric"]["impedance"].append(Z_new)

    if plot:
        def _plot(ax: Axes, x, y):
            for ix, iy, name in zip(x, y, data["name"]):
                ax.semilogx(ix, iy, label=name)

        plt.rcParams.update(default_styles)
        _, axs = plt.subplots(2, 2)
        # fig.suptitle(name)

        ax: Axes = axs[0][0]
        _plot(ax, data["acoustic"]["freq"], data["acoustic"]["spl"])
        ax.set_ylabel('SPL [dB]')
        ax.set_ylim((70, 120))

        ax: Axes = axs[1][0]
        _plot(ax, data["acoustic"]["freq"], data["acoustic"]["phase"])
        ax.set_ylabel('Phase [Degree]')
        ax.set_ylim((-200, +200))

        ax: Axes = axs[0][1]
        _plot(ax, data["electric"]["freq"], data["electric"]["impedance"])
        ax.set_ylabel('Impedance [Ohm]')

        ax: Axes = axs[1][1]
        _plot(ax, data["electric"]["freq"], data["electric"]["phase"])
        ax.set_ylabel('Phase [Degree]')
        ax.set_ylim((-200, +200))

        _axes_style(axs[0][0], fmin, fmax)
        _axes_style(axs[1][0], fmin, fmax)
        _axes_style(axs[0][1], fmin, fmax)
        _axes_style(axs[1][1], fmin, fmax)
        plt.show()
