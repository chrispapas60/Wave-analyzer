from record import keystroke_record, fixed_interval_record
from analysis import AudioFile
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

     
def record_audio():
    while True:
        def keystroke():
            print("Starting keystroke mode...\n")
            keystroke_record()
            return None

        def fixed_interval():
            print("Starting keystroke mode...\n")
            fixed_interval_record()
            return None

        def go_back():
            print("Returning to previous menu...")
            return True  # signal to the loop to break

        print ( # Print the menu
        "Choose keystroke or fixed interval recording.\n"
            "1. Keystroke\n"
            "2. Fixed interval\n"
            "3. Return to previous menu"
        )
    
        menu = {
            "1": keystroke,
            "2": fixed_interval,
            "3": go_back
        }

        choice = input("Make a selection: ") 
        action = menu.get(choice)
        if action:
            truefalse = action()
            if truefalse: # If the function in action is go_back (which returns true) truefalse is truthy and the loop will break
                break
        else: 
            print ("Invalid selection. Try again") # Else error and try again


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
from pathlib import Path

def analyse():

    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "outputs"

    if not output_dir.exists():
        print("No 'outputs' folder found.\n")
        return

    wav_files = list(output_dir.glob("*.wav"))

    if not wav_files:
        print("No WAV files found in outputs folder.\n")
        return

    # File Selection
    print("\nAvailable WAV files:\n")
    for i, file in enumerate(wav_files, start=1):
        print(f"{i}. {file.name}")

    while True:
        try:
            choice = int(input("\nSelect a file number (or 0 to go back): "))
            if choice == 0:
                return
            if 1 <= choice <= len(wav_files):
                selected_file = wav_files[choice - 1]
                break
            else:
                print("Invalid selection.")
        except ValueError:
            print("Enter a valid number.")

    # Load selected file
    audio = AudioFile(selected_file)

    # Analysis Submenu
    while True:
        print(
            "\nWhat would you like to do?\n"
            "1. Plot waveform\n"
            "2. Plot FFT\n"
            "3. Plot spectrogram\n"
            "4. Return to main menu"
        )

        action = input("Make a selection: ")

        if action == "1":
            audio.plot_waveform()

        elif action == "2":
            audio.plot_fft()

        elif action == "3":
            audio.spectrogram()

        elif action == "4":
            return

        else:
            print("Invalid selection.")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def exit_program():
    print("Farewell!")
    exit()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def main_menu():
    menu = {
        "1": record_audio,
        "2": analyse,
        "3": exit_program
    }

    while True:
        print(
            "Welcome to the Audio Analyser. How would you like to begin?\n"
            "1. Record audio\n"
            "2. Analyse audio\n"
            "3. Exit the program"
        )
        choice = input("Make a selection: ") 
        action = menu.get(choice) # menu.get checks the selection against the library and passes the corrosponding function to action
        # If the selection does not corrospond to a function, if returns None

        if action: # If action is a function, that function is called
            action()
        else: # If action is empty, and error is printed
            print ("Invalid selection. Try again")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


if __name__ == "__main__":
    main_menu()