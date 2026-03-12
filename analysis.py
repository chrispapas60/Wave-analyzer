import numpy as np
import wave
import matplotlib.pyplot as plt
plt.ion() # Turn on interactive mode to allow multiple functions to be plotted
from pathlib import Path


class AudioFile:

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self._load()

   
    def _load(self): # Loads the .wav file

        with wave.open(str(self.filepath), "rb") as wf:
            self.n_channels = wf.getnchannels()
            self.sample_width = wf.getsampwidth()
            self.sample_rate = wf.getframerate()
            self.n_frames = wf.getnframes()
            frames = wf.readframes(self.n_frames)

        self.duration = self.n_frames / self.sample_rate

        # Determine numpy dtype
        if self.sample_width == 1:
            dtype = np.uint8
        elif self.sample_width == 2:
            dtype = np.int16
        elif self.sample_width == 4:
            dtype = np.int32
        else:
            raise ValueError("Unsupported sample width")

        samples = np.frombuffer(frames, dtype=dtype) # The dtype allows numpy to interperet the raw bytes into specific integer data

        # Split stereo to mono if needed
        if self.n_channels == 2:
            self.left = samples[::2]
            self.right = samples[1::2]
        else:
            self.left = samples
            self.right = None

        self._normalize()

    # ---------------------------------
    # Normalize to [-1, 1]
    # ---------------------------------
    def _normalize(self):

        if self.sample_width == 1:
            self.left = (self.left - 128) / 128
        elif self.sample_width == 2:
            self.left = self.left / 32768
        elif self.sample_width == 4:
            self.left = self.left / 2147483648

    # ---------------------------------
    # Time axis
    # ---------------------------------
    def time_axis(self):
        return np.linspace(0, self.duration, len(self.left))

    # ---------------------------------
    # FFT
    # ---------------------------------
    def fft(self):

        fft_vals = np.fft.rfft(self.left)
        freqs = np.fft.rfftfreq(len(self.left), 1 / self.sample_rate)

        magnitude = np.abs(fft_vals)

        return freqs, magnitude

    # ---------------------------------
    # Plot waveform
    # ---------------------------------
    def plot_waveform(self, dark_mode=True):

        t = self.time_axis()

        if dark_mode:
            plt.style.use("dark_background")
            line_color = "#E7228E"
        else:
            plt.style.use("seaborn-v0_8")
            line_color = "#0EDBD1"

        fig, ax = plt.subplots(figsize=(12, 5), dpi=120)

        ax.plot(t, self.left, color=line_color, linewidth=0.7)
        ax.fill_between(t, self.left, 0, alpha=0.3)

        ax.set_title("Waveform", fontsize=16, weight="bold")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_ylim(-1.1, 1.1)
        ax.grid(True, alpha=0.15)

        plt.tight_layout()
        plt.show()

    # ---------------------------------
    # Plot FFT
    # ---------------------------------
    def plot_fft(self, dark_mode=True):

        freqs, magnitude = self.fft()

        if dark_mode:
            plt.style.use("dark_background")
            color = "#00F5D4"
        else:
            plt.style.use("seaborn-v0_8")
            color = "#003049"

        fig, ax = plt.subplots(figsize=(12, 5), dpi=120)

        ax.plot(freqs, magnitude, color=color, linewidth=0.8)
        ax.set_title("Frequency Spectrum (Magnitude)", fontsize=16, weight="bold")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.set_xlim(0, self.sample_rate / 2)

        plt.tight_layout()
        plt.show()

    # ---------------------------------
    # Spectrogram
    # ---------------------------------
    def spectrogram(self, dark_mode=True):

        if dark_mode:
            plt.style.use("dark_background")

        fig, ax = plt.subplots(figsize=(12, 5), dpi=120)

        Pxx, freqs, bins, im = ax.specgram(
            self.left,
            NFFT=1024,
            Fs=self.sample_rate,
            noverlap=512,
            cmap="magma"
        )

        ax.set_title("Spectrogram", fontsize=16, weight="bold")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")

        plt.colorbar(im).set_label("Intensity (dB)")

        plt.tight_layout()
        plt.show()


