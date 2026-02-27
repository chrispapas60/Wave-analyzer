# Wave-analyzer

-> INTRODUCTION
This project is a wave analyser which reads audio input from a microphone and outputs both numerical and graphical data about the captured sound waves. It has the following functions.

1) Audion capture
2) Analysis 
3) Real time streaming (not yet)

The main.py calls the other files.
The record.py class handles the intake of audio information from the device's microphone, and translates that information into a machine readable format(.WAV). 
Next, analysis.py reads the output of record.py and performs the requested mathematical calculations and outputs the amplitude, wave function, etc. of the sound wave.

-> INSTRUCTIONS

1) Download all the files
2) Place them on the same folder
3) Run main.py on visual code or simular enviroment
4) On the Serial consol you should see the menu with the options you have

-> Possible future updates 

1) Real time streaming mode
2) Display of more information such as peak amplitude/frequency
3) Addition of graphics and interactions
4) Process and comparition of multiple samples
