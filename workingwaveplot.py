import numpy as np
# real time microphone imput 
import sounddevice as sd

#wave plotting
import matplotlib.pyplot as plt

#live updating of the visual wave
from matplotlib.animation import FuncAnimation

#dominant frequency filter
from scipy.fft import fft

#run the plot without GUI freezing or bugging
from threading import Thread

# Audio Settings
# 44100 samples per second standard cd size 
SAMPLE_RATE = 44100
#2048 block so it runs smoothly, to large blocks = delay but better frequency 
#to small blocks, not precise enough
BLOCK_SIZE = 2048

is_recording = True
audio_data = np.zeros(BLOCK_SIZE)

# Audio Callback

# picks up new data from microphone automatically 
def audio_callback(indata, frames, time, status):
    global audio_data
    if is_recording:
        audio_data[:] = indata[:, 0]

# Start Audio Stream

stream = sd.InputStream(callback=audio_callback,
                        channels=1,
                        samplerate=SAMPLE_RATE,
                        blocksize=BLOCK_SIZE)
#active microphone listening
stream.start()


# Frequency Detection
#estimates dominant frequency 
#allows smoothness 
def detect_frequency(signal):
    window = np.hanning(len(signal))
    signal = signal * window
    
    fft_data = np.abs(fft(signal))
    #Computes frequency bins corresponding to FFT output.
    freq = np.fft.fftfreq(len(fft_data), 1/SAMPLE_RATE)

    
    #the wave/ FFT output is symmetric 
    #only half because we only need the positive 
    
    positive_freqs = freq[:len(freq)//2]
    magnitudes = fft_data[:len(freq)//2]

    magnitudes[0]=0
    
    #finds strongest component 
    peak_index = np.argmax(magnitudes)
    return positive_freqs[peak_index]


# Matplotlib Setup
#figure and axis creation
fig, ax = plt.subplots()
line, = ax.plot(audio_data)
#amplitude fixation
ax.set_ylim(-1, 1)
#title of the diagramm
ax.set_title("Live Audio Waveform")

#adds text in the plot

freq_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)


# Update Function

#regularely called by animation
def update(frame):
    line.set_ydata(audio_data)
    
    frequency = detect_frequency(audio_data)
    freq_text.set_text(f"Frequency: {frequency:.2f} Hz")
    
    return line,
#creates animation, more or less called every50ms so 20frames per second 
ani = FuncAnimation(fig, update, interval=50)
plt.show()
