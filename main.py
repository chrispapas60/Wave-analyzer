#Import recording methods from the input module 
#this fynctions handle the actual audio recording logic 
from input import keystroke_record, fixed_interval_record

class RecordAudioMenu:
    def record_audio(self):
        """
        Handles the audio recording menu 
        
        The user can choose between: 
        1. Recording triggered by keystrokes 
        2. Recording at fixed time intervals
        3.Returning to the main menu 
        """
        #Loops to keep the user inside the recording menu untill they choose to go back 
    while True:
        def keystroke():
            #start recording audio when a key is pressed 
            print("Starting keystroke mode...\n")
            keystroke_record()
            return None

        def fixed_interval():
            # Starts recording audio continuosly at fixed inervals 
            print("Starting keystroke mode...\n")
            fixed_interval_record()
            return None

        def go_back():
            # Return to the previous menu by breaking the loop 
            print("Returning to previous menu...")
            return True
        
        #Print the recording submenu
        print ( # Print the menu
        "Choose keystroke or fixed interval recording.\n"
            "1. Keystroke\n"
            "2. Fixed interval\n"
            "3. Return to previous menu"
        )
        
         # Diictionary that maps menu options to the corresponding function
        menu = {
            "1": keystroke,
            "2": fixed_interval,
            "3": go_back
        }

        # Ask the user for a choise 
        choice = input("Make a selection: ") 
        action = menu.get(choice)
        if action:
            truefalse = action()
            # if go_back() was selected, it returns True and we break the loop 
            if truefalse: 
                break
        else: 
            # if the user entered an invalid option 
            print ("Invalid selection. Try again") # Else error and try again


def analyse():
    pass

def exit_program():
    print("Farewell!")
    exit()

class MainMenu:
    """
    This class ahndels the main menu of the Audio Analyzer program.

    The main menu allows th euser to:
    1. Record audio 
    2. Analyse recorded audio
    3. Exit the program 
    """ 
    def main_menu(self):
        
    #Loop that keeps the program running until the user chooses to exit 
        while True:
            print(
            "Welcome to the Audio Analyser. How would you like to begin?\n"
            "1. Record audio\n"
            "2. Analyse audio\n"
            "3. Exit the program"
            )
            

   # Dictionary mapping user input corresponding function 
   # This allows the program to call the correct action based on the user's choice
            menu = {
            "1": record_audio,
            "2": analyse,
            "3": exit_program
            }

   
            # Ask the user to select an option 
            choice = input("Make a selection: ") 
            
            # menu.get checks the selection against the library and passes the corrosponding function to action
            # # If the selection does not corrospond to a function, if returns None
            action = menu.get(choice) 
    
            # If the user selected a valid option, execute the corresponding function 
            if action: 
                action()
            else: 
                # If the user entered an invalid option 
                print ("Invalid selection. Try again")


if __name__ == "__main__":
    menu = MainMenu()
    Menu.main_menu()
