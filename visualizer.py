import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.fft import fft


def live_visualizer():

    SAMPLE_RATE = 44100
    BLOCK_SIZE = 2048

    is_recording = True
    audio_data = np.zeros(BLOCK_SIZE)

    # -----------------------
    # Audio callback
    # -----------------------
    def audio_callback(indata, frames, time, status):
        nonlocal audio_data
        audio_data[:] = indata[:, 0]

    # -----------------------
    # Frequency detection
    # -----------------------
    def detect_frequency(signal):
        window = np.hanning(len(signal))
        signal = signal * window

        fft_data = np.abs(fft(signal))
        freq = np.fft.fftfreq(len(fft_data), 1/SAMPLE_RATE)

        positive_freqs = freq[:len(freq)//2]
        magnitudes = fft_data[:len(freq)//2]
        magnitudes[0] = 0

        peak_index = np.argmax(magnitudes)
        return positive_freqs[peak_index]

    # -----------------------
    # Start stream
    # -----------------------
    stream = sd.InputStream(callback=audio_callback,
                            channels=1,
                            samplerate=SAMPLE_RATE,
                            blocksize=BLOCK_SIZE)

    stream.start()

    # -----------------------
    # Matplotlib setup
    # -----------------------
    fig, ax = plt.subplots()
    line, = ax.plot(audio_data)
    ax.set_ylim(-1, 1)
    ax.set_title("Live Audio Waveform")
    freq_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    # -----------------------
    # Update function
    # -----------------------
    def update(frame):
        line.set_ydata(audio_data)
        frequency = detect_frequency(audio_data)
        freq_text.set_text(f"Frequency: {frequency:.2f} Hz")
        return line,

    ani = FuncAnimation(fig, update, interval=50)

    plt.show()

   # stop stream after closing window
    stream.stop()
    stream.close()
