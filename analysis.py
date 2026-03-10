import numpy as np
import scipy as sp
import struct
import wave
import matplotlib.pyplot as plt
from pathlib import Path

# Find the path of the current script and define the WAV file to analyze 
script_dir = Path(__file__).resolve().parent 
filepath = script_dir / "output.wav"


class audio_input_file:
    """
    Represents an input audio file and stores its file information.

    Attributes:
        fname: Name of the file
        ftype: Type of file (currently expected to be '.wav')
        fpath: Full path to the audio file
    """
     
    def __init__(self, fname, ftype):
        self.fname = fname
        self.ftype = ftype 
        self.fpath = script_dir / fname
    
    def get_metadata(self):
         """
        Open the WAV file and extract its basic metadata.

        Returns:
            n_channels, sample_width, sample_rate, n_frames
        """
         with wave.open(str(filepath), "rb") as wf :
            n_channels = wf.getnchannels() # 1 = mono, 2 = stereo
            sample_width = wf.getsampwidth() # bytes per sample
            sample_rate = wf.getframerate() #samples per second
            n_frames = wf.getnframes() # total number of frames

            return n_channels, sample_width, sample_rate, n_frames
     
    def get_frames(self):
        """
        Read the raw audio frames from the WAV file.

        Returns:
            Raw binary frame data
        """
        with wave.open(str(self.fpath), "rb") as wf:
            frames = wf.readframes(wf.getnframes())

        return frames
         
class audio_object: 
    """
    Represents a loaded audio file and stores its basic metadata.

    Attributes:
        n_channels: Number of audio channels (1 = mono, 2 = stereo)
        sample_width: Number of bytes used per sample
        sample_rate: Number of samples per second
        n_frames: Total number of audio frames in the file
    """
    def __init__(self, n_channels, sample_width, sample_rate, n_frames,):
    # Initialize an audio_object instance with the main audio properties

        self.n_channels = n_channels
        self.sample_width = sample_width
        self.sample_rate = sample_rate
        self.n_frames = n_frames 

# Create an input file object and extract its metadata 
audio_file = audio_input_file("output.wav", ".wav")
n_channels, sample_width, sample_rate, n_frames = audio_file.get_metadata()
frames = audio_file.get_frames()

#store the extracted metadata in an audio_object instance
audio = audio_object(n_channels, sample_width, sample_rate, n_frames)

#Determine the correct struct format string based on sample width 
if audio.sample_width == 1:
    fmt = "<{}B".format(audio.n_frames * audio.n_channels)
elif audio.sample_width == 2:
    fmt = "<{}h".format(audio.n_frames * audio.n_channels)
elif audio.sample_width == 4:
    fmt = "<{}i".format(audio.n_frames * audio.n_channels)
else:
    raise ValueError("Unsupported sample width: {}".format(audio.sample_width))

#  Convert the raw binary frame data into a NumPy array of samples 
samples = np.array(struct.unpack(fmt, frames))

#Split the data if the audio is stereo 
if n_channels == 2:
    left = samples[::2]
    right = samples[1::2]
else:
    left = samples
    right = None

# Normalize sample values to the range [-1, 1]
if sample_width == 1:
    left = (left - 128) / 128  # 8-bit samples are unsigned, so shift values before normalization 
elif sample_width == 2:
    left = left / 32768       
elif sample_width == 4:
    left = left / 2147483648   

# Plot the waveform of the left channel 
fig, ax = plt.subplots()
ax.plot(left, '-')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.show()

