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


"""
This class contains the audio input methods of the program 

It includes:
1. Keystroke-based recording 
2. Fixed-interval recording 
"""

def keystroke_record():
     """
     Record audio untill the user presses the space bar again. 

     This method starts recording when the user preses SPACE and stops when SPACE is pressed a second time. 
     """

     sample_form = pyaudio.paInt16
     sr = 44100
     channels = 1
     chunk = 1024

     # Create a PyAudio object to acess the microphone input stream 
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

     # Keep collecting audio chunks untill the user presses SPACE again
     while recording:
          data = stream.read(chunk)
          frames.append(data)

          if keyboard.is_pressed("space"):
               recording = False

     print("Recording stopped.")

     # Stop and close the audio stream after recording ends
     stream.stop_stream()
     stream.close()

     p.terminate()
     
     # Build the full output path for the .wav file
     wave_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", f"{fname}.wav")

     wf = wave.open(wave_out, 'wb')
     wf.setnchannels(channels)
     wf.setsampwidth(p.get_sample_size(sample_form))
     wf.setframerate(sr)
     wf.writeframes(b''.join(frames))
     wf.close()

     print("Saved to" , wave_out) # Print location where file was saved

     
def fixed_interval_record():
     """
     Record Audio for a user-defined number of seconds. 

     The user is asked to enter a duration between 1 and 60 seconds. 
     A counter is shown while recording, and the audio is saved as .wav file.
     """

     while True:
          try: # Checks if duration is acceptable, if so break, if not print error
               duration = int(input("How many seconds do you want to record? "))
               if 0 < duration < 61: # Could make a variable here so max time can be changed, a bit overkill tho
                    break
          except:
               print("Invalid input. Please enter an integer between 1 and 60")

def counter(duration):
     #Dispaly a live second-by-second counter while recording 
     for i in range(1, duration + 1):
          print(f"Recording... {i}", end='\r')  # '\r' overwrites the line
          time.sleep(1)  # wait 1 second

     print("\nRecording finished!")

def record(duration):
     # Record audio for the specified duration and save it as a .wav file.
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

