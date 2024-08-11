import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter

from akustik.plot.style import default_styles


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


def axes_style(ax: Axes, fmin, fmax):
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_xlabel('Frequency [Hz]')
    ax.set_xlim((fmin, fmax))
    ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.5)
    ax.minorticks_on()

    return ax


def report(frd_file, zma_file, fmin, fmax):
    FR = read_dats_frequency_response(frd_file)
    IR = read_dats_impedance_response(zma_file)

    frequency = FR["Frequency"].to_numpy()
    spl = FR["SPL"].to_numpy()
    phase = FR["Phase"].to_numpy()

    plt.rcParams.update(default_styles)
    fig, axs = plt.subplots(2, 2)
    fig.suptitle("Dayton Audio 15\" RSS390HF-4")

    ax: Axes = axs[0][0]
    ax.semilogx(frequency, spl)
    ax.set_ylabel('SPL [dB]')
    ax.set_ylim((70, 120))

    ax: Axes = axs[1][0]
    ax.semilogx(frequency, phase)
    ax.set_ylabel('Phase [Degree]')

    frequency = IR["Frequency"].to_numpy()
    impedance = IR["Impedance"].to_numpy()
    phase = IR["Phase"].to_numpy()
    P_amp = 150

    ax: Axes = axs[0][1]
    ax.semilogx(frequency, impedance)
    ax.set_ylabel('Impedance [Ohm]')

    ax: Axes = axs[1][1]
    ax.semilogx(frequency, phase)
    ax.set_ylabel('Phase [Degree]')

    axes_style(axs[0][0], fmin, fmax)
    axes_style(axs[1][0], fmin, fmax)
    axes_style(axs[0][1], fmin, fmax)
    axes_style(axs[1][1], fmin, fmax)
    plt.show()
