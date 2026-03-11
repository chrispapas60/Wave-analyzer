from record import keystroke_record, fixed_interval_record
from analysis import AudioFile
from pathlib import Path


# Simple reusable menu class
# It takes a title and a dictionary of options and runs the menu loop
class Menu:

    def __init__(self, title, options):
        self.title = title
        self.options = options  # dictionary: "choice": (description, function)

    def display(self):

        while True:
            print("\n" + self.title)

            # print each menu option
            for key, (desc, _) in self.options.items():
                print(f"{key}. {desc}")

            choice = input("Make a selection: ")
            action = self.options.get(choice)

            if action:
                func = action[1]

                # if function is None we treat it as "go back"
                if func is None:
                    return

                func()
            else:
                print("Invalid selection. Try again")


# Handles recording features
class Recorder:

    # Recording triggered by pressing a key
    def keystroke(self):
        print("Starting keystroke mode...\n")
        keystroke_record()

    # Recording at fixed time intervals
    def fixed_interval(self):
        print("Starting fixed interval mode...\n")
        fixed_interval_record()

    # Opens the recording menu
    def menu(self):

        menu = Menu(
            "Choose recording mode:",
            {
                "1": ("Keystroke", self.keystroke),
                "2": ("Fixed interval", self.fixed_interval),
                "3": ("Return to previous menu", None)
            }
        )

        menu.display()


# Handles loading and analysing audio files
class Analyzer:

    # Finds all wav files inside the outputs folder
    def get_wav_files(self):

        script_dir = Path(__file__).resolve().parent
        output_dir = script_dir / "outputs"

        if not output_dir.exists():
            print("No 'outputs' folder found.\n")
            return []

        return list(output_dir.glob("*.wav"))

    # Lets the user pick which file to analyse
    def select_file(self):

        wav_files = self.get_wav_files()

        if not wav_files:
            print("No WAV files found in outputs folder.\n")
            return None

        print("\nAvailable WAV files:\n")

        for i, file in enumerate(wav_files, start=1):
            print(f"{i}. {file.name}")

        while True:
            try:
                choice = int(input("\nSelect a file number (or 0 to go back): "))

                if choice == 0:
                    return None

                if 1 <= choice <= len(wav_files):
                    return wav_files[choice - 1]

                print("Invalid selection.")

            except ValueError:
                print("Enter a valid number.")

    # Analysis submenu for a selected file
    def analysis_menu(self, audio):

        menu = Menu(
            "What would you like to do?",
            {
                "1": ("Plot waveform", audio.plot_waveform),
                "2": ("Plot FFT", audio.plot_fft),
                "3": ("Plot spectrogram", audio.spectrogram),
                "4": ("Return to main menu", None)
            }
        )

        menu.display()

    # Main analysis workflow
    def run(self):

        selected_file = self.select_file()

        if selected_file is None:
            return

        audio = AudioFile(selected_file)

        self.analysis_menu(audio)


# Controls the overall program flow
class Program:

    def __init__(self):
        self.recorder = Recorder()
        self.analyzer = Analyzer()

    # Ends the program
    def exit_program(self):
        print("Farewell!")
        exit()

    # Main menu shown when the program starts
    def main_menu(self):

        menu = Menu(
            "Welcome to the Audio Analyser. How would you like to begin?",
            {
                "1": ("Record audio", self.recorder.menu),
                "2": ("Analyse audio", self.analyzer.run),
                "3": ("Exit the program", self.exit_program)
            }
        )

        menu.display()


# Ensures the program only runs when this file is executed directly
if __name__ == "__main__":
    program = Program()
    program.main_menu()
