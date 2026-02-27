import numpy as np
import wave 
import pyaudio
import os
from datetime import datetime # Here I'm importing the datetime class from within the module datetime
import time
import threading
import keyboard

# Get current date and time
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S") #Save string "year-month-day_hour-minute-second"
fname = timestamp # Generic filename variable to hold the timestamp string, for when renaming files functionality added


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


def keystroke_record():
     sample_form = pyaudio.paInt16
     sr = 44100
     channels = 1
     chunk = 1024

     p = pyaudio.PyAudio()

     print("Press SPACE to start recording...")
     keyboard.wait("space") # Waits for spacebar input

     print("Recording... Press SPACE again to stop.")

     stream = p.open(format=sample_form,
                         channels=channels,
                         rate=sr,
                         frames_per_buffer=chunk,
                         input=True,)
          
     frames = []
     recording = True

     while recording:
          data = stream.read(chunk)
          frames.append(data)

          if keyboard.is_pressed("space"):
               recording = False

     print("Recording stopped.")

     stream.stop_stream()
     stream.close()

     p.terminate()
     
     wave_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", f"{fname}.wav")

     wf = wave.open(wave_out, 'wb')
     wf.setnchannels(channels)
     wf.setsampwidth(p.get_sample_size(sample_form))
     wf.setframerate(sr)
     wf.writeframes(b''.join(frames))
     wf.close()

     print("Saved to" , wave_out) # Print location where file was saved

     
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


def fixed_interval_record():
     while True:
          try: # Checks if duration is acceptable, if so break, if not print error
               duration = int(input("How many seconds do you want to record? "))
               if 0 < duration < 61: # Could make a variable here so max time can be changed, a bit overkill tho
                    break
          except:
               print("Invalid input. Please enter an integer between 1 and 60")

     def counter(duration):
          for i in range(1, duration + 1):
               print(f"Recording... {i}", end='\r')  # '\r' overwrites the line
               time.sleep(1)  # wait 1 second

          print("\nRecording finished!")

     def record(duration):
          sample_form = pyaudio.paInt16
          sr = 44100
          channels = 1
          chunk = 1024

          #Stores concatenated string of parent directory + filename + .wav 
          wave_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", f"{fname}.wav")

          p = pyaudio.PyAudio() 

          stream = p.open(format=sample_form,
                         channels=channels,
                         rate=sr,
                         frames_per_buffer=chunk,
                         input=True,)
          
          frames = []
          for i in range(0,int(sr/chunk * duration)) :
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

          print("Saved to" , wave_out) # Print location where file was saved

     counter_thread = threading.Thread(target=counter, args=(duration,))

     # Both counter and record run simultaneously using threading
     counter_thread.start()
     record(duration)

