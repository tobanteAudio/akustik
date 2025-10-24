import sys

import matplotlib.pyplot as plt
import numpy as np

from akustik.speaker.dats import read_dats_folder, _axes_style


def main():
    name, frd, zma = read_dats_folder(sys.argv[1])

    f: np.ndarray = zma["Frequency"].to_numpy()
    Z: np.ndarray = zma["Impedance"].to_numpy()
    V = 2.83
    P = (V**2)/Z
    I = V/Z

    ax = plt.gca()
    ax.semilogx(f, Z, label=name)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Impedance [Ohm]')
    ax.set_title('Impedance')
    _axes_style(ax, 10, 20000)
    plt.show()

    ax = plt.gca()
    ax.semilogx(f, P, label=name)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Power [W]')
    ax.set_title(f'Power @ {V} V')
    _axes_style(ax, 10, 20000)
    plt.show()

    ax = plt.gca()
    ax.semilogx(f, I, label=name)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Current [A]')
    ax.set_title(f'Current @ {V} V')
    _axes_style(ax, 10, 20000)
    plt.show()

    p = np.linspace(0.1, 500, len(f))
    inV = np.sqrt(p*4)/(10**(25.6/20))
    indBu = 20*np.log10(inV/0.7746)
    ax = plt.gca()
    ax.plot(p, indBu, label=name)
    ax.set_xlabel('Power [W]')
    ax.set_ylabel('Voltage [dBu]')
    ax.set_title(f'Input Voltage')
    _axes_style(ax, 0.1, 500)
    plt.show()


main()
