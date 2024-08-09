import pathlib

import h5py
import matplotlib.pyplot as plt
import numpy as np
from resampy import resample
import scipy.signal as signal

from akustik.diffusor.measurement import polar_response


def _resample(x, Fs_original, Fs_target=48_000):
    if Fs_original == Fs_target:
        x, Fs_original
    x = resample(x, Fs_original, Fs_target, filter='kaiser_best')
    return x, Fs_target


def main(sim_dir):
    sim_dir = pathlib.Path(sim_dir)
    out_file = sim_dir / "out.h5"

    sim_file = h5py.File(sim_dir / "sim.h5", 'r')
    fs = float(sim_file['fs'][...])

    file = h5py.File(out_file, 'r')
    out = file['out'][...]
    out, fs = _resample(out, fs)

    fmax = float(sim_file['fmax'][...])
    fmin = 125.0
    trim_ms = 20
    trim_samples = int(fs/1000*trim_ms)

    print(f"{out_file=}")
    print(f"{fs=:.3f} Hz")
    print(f"len={out.shape[1]/fs:.2f} s")
    print(f"{trim_ms=}")
    print(f"{trim_samples=}")
    print(f"{out.shape=}")

    out = out[:, trim_samples:]

    sos = signal.butter(4, fmin, fs=fs, btype='high', output='sos')
    out = signal.sosfiltfilt(sos, out)

    sos = signal.butter(4, fmax, fs=fs, btype='low', output='sos')
    out = signal.sosfiltfilt(sos, out)

    out *= signal.windows.hann(out.shape[1])
    spectrum = np.fft.rfft(out, axis=-1)
    frequencies = np.fft.rfftfreq(out.shape[1], 1/fs)
    times = np.linspace(0.0, out.shape[1]/fs, out.shape[1])

    dB = 20*np.log10(np.abs(spectrum)+np.spacing(1))
    dB = dB-np.max(dB)

    plt.plot(times, out[15, :], label=f'{15}deg')
    plt.plot(times, out[45, :], label=f'{45}deg')
    plt.plot(times, out[90, :], label=f'{90}deg')
    plt.grid()
    plt.legend()
    plt.show()

    plt.semilogx(frequencies, dB[15, :], label=f'{15}deg')
    plt.semilogx(frequencies, dB[45, :], label=f'{45}deg')
    plt.semilogx(frequencies, dB[90, :], label=f'{90}deg')
    plt.xlim((10, fmax*2))
    plt.ylim((-60, 0))
    plt.grid()
    plt.legend()
    plt.show()

    rms_values, mic_angles = polar_response(out, fs, 0, 180, trim_angle=15)

    fig, ax = plt.subplots(
        3, 2,
        constrained_layout=True,
        subplot_kw={'projection': 'polar'}
    )
    fig.suptitle(f"Diffusion")

    ax[0][0].plot(np.deg2rad(mic_angles), rms_values[0][0])
    ax[0][0].set_title(rms_values[0][1])
    ax[0][0].set_ylim((0.0, 100.0))
    ax[0][0].set_thetamin(0)
    ax[0][0].set_thetamax(180)

    ax[0][1].plot(np.deg2rad(mic_angles), rms_values[1][0])
    ax[0][1].set_title(rms_values[1][1])
    ax[0][1].set_ylim((0.0, 100.0))
    ax[0][1].set_thetamin(0)
    ax[0][1].set_thetamax(180)

    ax[1][0].plot(np.deg2rad(mic_angles), rms_values[2][0])
    ax[1][0].set_title(rms_values[2][1])
    ax[1][0].set_ylim((0.0, 100.0))
    ax[1][0].set_thetamin(0)
    ax[1][0].set_thetamax(180)

    ax[1][1].plot(np.deg2rad(mic_angles), rms_values[3][0])
    ax[1][1].set_title(rms_values[3][1])
    ax[1][1].set_ylim((0.0, 100.0))
    ax[1][1].set_thetamin(0)
    ax[1][1].set_thetamax(180)

    ax[2][0].plot(np.deg2rad(mic_angles), rms_values[4][0])
    ax[2][0].set_title(rms_values[4][1])
    ax[2][0].set_ylim((0.0, 100.0))
    ax[2][0].set_thetamin(0)
    ax[2][0].set_thetamax(180)

    ax[2][1].plot(np.deg2rad(mic_angles), rms_values[5][0])
    ax[2][1].set_title(rms_values[5][1])
    ax[2][1].set_ylim((0.0, 100.0))
    ax[2][1].set_thetamin(0)
    ax[2][1].set_thetamax(180)

    plt.show()


if __name__ == '__main__':
    main()
