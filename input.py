import numpy as np
import wave 
import pyaudio
import struct
import matplotlib.pyplot as plt

sample_form = pyaudio.paInt16
sr = 44100
channels = 1
sec = 5
chunk = 1024
wave_out = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=sample_form,
                channels=channels,
                rate=sr,
                frames_per_buffer=chunk,input=True, output=True)
print("rec")
frames = []
for i in range(0,int(sr/chunk * sec)) :
     data = stream.read(chunk)
     frames.append(data)

stream.stop_stream()
stream.close()

p.terminate()

wf = wave.open(wave_out, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_form))
wf.setframerate(sr)
wf.writeframes(b''.join(frames))
wf.close()
