import sounddevice as sd
import numpy as np

# Standard guitar string frequencies (in Hertz)
GUITAR_STRINGS = {
    "E2 (Low E)": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4 (High E)": 329.63
}

SAMPLE_RATE = 44100  # Standard audio sampling rate
FRAMES = 2048        # Number of audio frames per chunk
VOLUME_THRESHOLD = 5  # Minimum volume to trigger the tuner


def find_closest_string(freq):
    """Finds the closest standard guitar string to the detected frequency."""
    closest_string = min(GUITAR_STRINGS.keys(),
                         key=lambda k: abs(GUITAR_STRINGS[k] - freq))
    target_freq = GUITAR_STRINGS[closest_string]
    difference = freq - target_freq
    return closest_string, target_freq, difference


def audio_callback(indata, frames, time, status):
    """This function is called for every audio chunk captured by the mic."""
    if status:
        print(status)

    # Flatten the audio data to a 1D array
    audio_data = indata[:, 0]

    # Apply a window function (Hanning) to smooth the audio chunk edges
    windowed_data = audio_data * np.hanning(len(audio_data))

    # Perform Fast Fourier Transform (FFT) to extract frequencies
    fft_result = np.fft.rfft(windowed_data)
    frequencies = np.fft.rfftfreq(len(windowed_data), 1.0 / SAMPLE_RATE)

    # Calculate the magnitude of each frequency
    magnitudes = np.abs(fft_result)

    # Find the frequency with the highest magnitude (the loudest pitch)
    peak_index = np.argmax(magnitudes)
    peak_freq = frequencies[peak_index]

    # Filter out background noise and ignore frequencies outside a guitar's range
    if np.max(magnitudes) > VOLUME_THRESHOLD and 70 < peak_freq < 400:
        string_name, target_freq, diff = find_closest_string(peak_freq)

        # Determine tuning direction
        if abs(diff) < 1.5:
            tune_status = "🟢 IN TUNE"
        elif diff > 0:
            tune_status = "👇 TUNE DOWN"
        else:
            tune_status = "👆 TUNE UP"

        # Print the result to the console
        print(
            f"Detected: {peak_freq:5.1f} Hz | Target: {string_name:11} ({target_freq:6.2f} Hz) | {tune_status}")


print("🎸 Starting Guitar Tuner... Play a string! (Press Ctrl+C to stop)")

try:
    # Open the microphone stream
    with sd.InputStream(channels=1, callback=audio_callback, samplerate=SAMPLE_RATE, blocksize=FRAMES):
        while True:
            # Keep the script running
            sd.sleep(1000)
except KeyboardInterrupt:
    print("\n🛑 Tuner stopped.")
except Exception as e:
    print(f"\n❌ An error occurred: {e}")
