import numpy as np
import wave 
import pyaudio
import os
from datetime import datetime # Here I'm importing the datetime class from within the module datetime
import time
import threading

# Get current date and time
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



import os
import wave
import pyaudio
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def keystroke_record():
    sample_form = pyaudio.paInt16
    sr = 44100
    channels = 1
    chunk = 1024

    # Ask for filename
    while True:
          temp = input("Do you want to name the file? (y/n): ").strip().lower()
          if temp == "y":
            fname = input("Enter new filename: ").strip()
            break  # exit the loop
          elif temp == "n":
            fname = get_timestamp()
            break  # exit the loop
          else:
              print("Invalid input. Please enter 'y' or 'n'.")

    # Ensure outputs folder exists
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    wave_out = os.path.join(output_dir, f"{fname}.wav")

    # Wait for user to start recording
    input("Press Enter to start recording...")

    print("Recording... Press Enter again to stop.")

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_form,
                    channels=channels,
                    rate=sr,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    # Record until user presses Enter
    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
            # Non-blocking check for Enter
            if os.name == "nt":  # Windows
                import msvcrt
                if msvcrt.kbhit() and msvcrt.getch() == b'\r':
                    break
            else:  # macOS / Linux
                import sys, select
                if select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.readline()
                    break
    except KeyboardInterrupt:
        # Allow Ctrl+C to stop recording
        pass

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    sampwidth = p.get_sample_size(sample_form)
    p.terminate()

    # Save to WAV
    with wave.open(wave_out, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sr)
        wf.writeframes(b''.join(frames))

    print("Saved to", wave_out)

     
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


def fixed_interval_record():
     while True:
          try: # Checks if duration is acceptable, if so break, if not print error
               duration = int(input("How many seconds do you want to record? "))
               if 0 < duration < 61: # Could make a variable here so max time can be changed, a bit overkill tho
                        while True:
                         temp = input("Do you want to name the file? (y/n): ").strip().lower()
                         if temp == "y":
                              fname = input("Enter new filename: ").strip()
                              break  # exit the loop
                         elif temp == "n":
                              fname = get_timestamp()
                              break  # exit the loop
                         else:
                              print("Invalid input. Please enter 'y' or 'n'.")
                              
                   #print("Do you want to name the file? (y/n)")
                   #while 1:
                     #temp = input()
                     #if temp.lower() == "y":
                          #print("Enter new filename: ")
                          #fname = input()
                          #break
                   #else :
                          #fname = get_timestamp # If user doesn't want to rename, use the timestamp as the filename
                          #break
      
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





