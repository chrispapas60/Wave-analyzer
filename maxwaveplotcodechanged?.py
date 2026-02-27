from time import time

import numpy as np
import scipy as sp
import struct
import wave
import matplotlib.pyplot as plt
from pathlib import Path

#After this make this input into a variable storing a .wav file so multiple/any .wav files can be saved and used
#Maybe better to make this a class with a class function doing the below, then can store new .wav files as instances of that class and operate on them thusly

scr_dir = Path(__file__).resolve().parent
filepath = scr_dir / "output.wav"

#Using pythons Wave module to parse the .wav file, the "rb" tag means read binary
with wave.open(str(filepath), "rb") as wf :

    def __init__(self, fname, ftype):
        self.fname = fname
        self.ftype = ftype #should be 3 options ".wav" "mp3" etc
        self.fpath = script_dir / fname 

    def filename(self):
        return self.fname
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


class audio_object: # This will be any instance of audio, we will pull it's data and store it as this class

    def __init__(self, n_channels, sample_width, sample_rate, n_frames,):
        
        self.n_channels = n_channels
        self.sample_width = sample_width
        self.sample_rate = sample_rate
        self.n_frames = n_frames 



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#so, this module should act on a class object called audio_input_file, which will have a filetype and a filepath
#It will pull the ftype and then pull the data accordingly (now only .wav)
#Then, it will make a new instance of the audio_object class, filling all the requisite variables


# Finds path of currently running program, gets it's parent directory
script_dir = Path(__file__).resolve().parent
filepath = script_dir / "output.wav"

# Wave module parses the .wav file, "rb" tag -> read binary
with wave.open(str(filepath), "rb") as wf :

    n_channels = wf.getnchannels() # Channel info (1 -> mono, 2 -> sterio)
    sample_width = wf.getsampwidth() # Sample width (1 -> 8 bit, 2 -> 16 bit, 4 -> 32 bit)
    sample_rate = wf.getframerate() # Samples per second
    n_frames = wf.getnframes() # Number of frames

# The framerate is stored as fmt with the correct struct format string depending on if it is 8, 16, or 32 bit
if sample_width == 1:
    fmt = "<{}B".format(n_frames * n_channels)
elif sample_width == 2:
    fmt = "<{}h".format(n_frames * n_channels)
elif sample_width == 4:
    fmt = "<{}i".format(n_frames * n_channels)
# Print's error if sample width is not 8, 16, or 32 bit
else:
    raise ValueError("Unsupported sample width: {}".format(sample_width))

# Finally, struct unpacks the data from the fmt and frames variables into a numpy array stored in the variable samples
frames = wf.readframes(n_frames)
samples = np.array(struct.unpack(fmt, frames))

#Split the data if it's stereo in preparation for fourier transform
if n_channels == 2:
    left = samples[::2]
    right = samples[1::2]
else:
    left = samples
    right = None

# Normalize sample values between -1, 1
if sample_width == 1:
    left = (left - 128) / 128  # 8-bit samples are unsigned --> subtract 128 to shift values from 0, 256 to -128, 128
elif sample_width == 2:
    left = left / 32768        # 16-bit samples signed between - and + 32768
elif sample_width == 4:
    left = left / 2147483648   # 32-bit signed - and + 2147483648

plt.style.use("dark_background")


fig, ax = plt.subplots(figsize=(12, 5), dpi=120)

ax.plot(time, left, color="#00FFAA", linewidth=0.7)
ax.fill_between(time, left, 0, alpha=0.3)

ax.set_title("Live Waveform", fontsize=16, weight="bold")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")

ax.set_ylim(-1.1, 1.1)
ax.grid(True, alpha=0.15)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()
