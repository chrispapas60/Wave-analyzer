import pyaudio 
import numpy as np
import scipy as sp
import struct
import wave


#Using pythons Wave module to parse the .wav file, the "rb" tag means read binary
with wave.open("output.wav", "rb") as wf :

#Important data of the .wav file is stored in variables
#Channel info (1,2 --> mono, sterio) as n_channels
#Sample width (1,2,4...(bytes) --> 8 bit, 16 bit, 32 bit ...) as sample_width
#Samples per second (44100, 48000, 96000 etc) as sample_rate
#Number of frames as n_frames
    n_channels = wf.getchannels()
    sample_width = wf.getsampwidth()
    sample_rate = wf.getframerate()
    n_frames = wf.getnframes()

#Then the wf.readframes command reads audio data in the .wav file and returns those bytes in the variable frames 
    frames = wf.readframes(n_frames)

#The framerate is stored as fmt with the struct format string "<{}B,h, or i " to denote  Little-endian and B,h, or i depending on the sample width (to denote 8, 16, or 32 bit samples)
if sample_width == 1:
    fmt = "<{}B".format(n_frames * n_channels)
elif sample_width == 2:
    fmt = "<{}h".format(n_frames * n_channels)
elif sample_width == 4:
    fmt = "<{}i".format(n_frames * n_channels)
#Print's error if sample width is not 8, 16, or 32 bit
else:
    raise ValueError("Unsupported sample width: {}".format(sample_width))

#Finally, struct unpacks the data from the fmt and frames variables into a numpy array stored in the variable samples
samples = np.array(struct.unpack(fmt, frames))

#Split the data if it's stereo in preparation for fourier transform
if n_channels == 2:
    left = samples[::2]
    right = samples[1::2]
else:
    left = samples
    right = None

#Normalize values of sample to between -1 and 1
if sample_width == 1:
    left = (left - 128) / 128  # 8-bit samples are unsigned, so -128 to shift values from 0, 256 to -128, 128 first
elif sample_width == 2:
    left = left / 32768        # 16-bit samples are between - and + 32768
elif sample_width == 4:
    left = left / 2147483648   # 32-bit signed - and + 2147483648

fig, ax = plt.subplots()
ax.plot(left, '-')
plt.show()
