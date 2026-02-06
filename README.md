# Wave-analyzer

This project is a wave analyser which reads audio input from a microphone and outputs both numerical and graphical data about the captured sound waves. It has the following functions.

1) Audion capture
2) Analysis (frequency, amplitude, waveform graph and maybe a spectrogram)
3) Real time streaming

The program uses 4 classes: main.py, input.py, analysis.py, visualization.py.

The main.py class calls the other classes.
The input.py class handles the intake of audio information from the device's microphone, and translates that information into a machine readable format. 
Next, analysis.py reads the output of input.py and performs the requiste mathematical and outputs the period, amplitude, wave function, etc. of the sound wave.
Finally, visualization.py reads analysis.py's outputs and displays a visualization of the information.

