import click
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

@click.group(help="Active noise cancellation.",invoke_without_command=True)
def anc():
    # Parameters
    fs = 44100  # Sampling rate
    M = 64  # Length of the adaptive filter
    mu = 0.001  # Step size for the LMS algorithm
    N = 10000  # Number of samples to process

    # Simulate signals
    # Generate a low-frequency noise signal (below 100Hz)
    t = np.arange(N) / fs
    noise_freq = 50  # Frequency in Hz
    mic_top = np.sin(2 * np.pi * noise_freq * t)  # Simulated noise from the top mic
    mic_bottom = mic_top + 0.5 * np.random.randn(N)  # Simulated noise plus some random noise

    # Initialize adaptive filter weights
    w = np.zeros(M)
    output_signal = np.zeros(N)
    error_signal = np.zeros(N)

    # LMS algorithm to adaptively filter the signal
    for n in range(M, N):
        x_n = mic_top[n:n-M:-1]  # Get the current segment of the input signal
        output_signal[n] = np.dot(w, x_n)  # Compute the filter output
        error_signal[n] = mic_bottom[n] - output_signal[n]  # Compute the error
        w += 2 * mu * error_signal[n] * x_n  # Update the filter coefficients

    # # Plot the results
    # plt.plot(t, mic_bottom, label='Original Signal (Bottom Mic)')
    # plt.plot(t, output_signal, label='Filtered Signal (Output)')
    # plt.plot(t, error_signal, label='Error Signal (After Cancellation)')
    # plt.title('LMS Active Bass Absorption')
    # plt.xlabel('Time [s]')
    # plt.ylabel('Amplitude')
    # plt.legend()
    # plt.show()

    # Plot the results
    freq = np.fft.rfftfreq(N,1/fs)

    mic_fft = np.fft.rfft(mic_bottom)
    output_fft = np.fft.rfft(output_signal)
    error_fft = np.fft.rfft(error_signal)

    mic_spl = 20*np.log10(np.abs(mic_fft))
    output_spl = 20*np.log10(np.abs(output_fft))
    error_spl = 20*np.log10(np.abs(error_fft))

    # mic_phase = np.rad2deg(np.angle(mic_fft))
    # output_phase = np.rad2deg(np.angle(output_fft))
    # error_phase = np.rad2deg(np.angle(error_fft))

    plt.semilogx(freq, mic_spl, label='Original Signal (Bottom Mic)')
    plt.semilogx(freq, output_spl, label='Filtered Signal (Output)')
    plt.semilogx(freq, error_spl, label='Error Signal (After Cancellation)')
    plt.title('LMS Active Bass Absorption')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('SPL [dB]')
    plt.legend()
    plt.grid(which="both")
    plt.xlim((1,30_000))
    plt.show()
