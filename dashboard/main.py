from app.cli_menu_logic import cli_menu_logic
#Function to display the encounters and ask for feedback using

print("--------------------------------------------------")
print(r"""
    ______      _          _____ _               _
    | ___ \    | |        /  __ \ |             | |   
    | |_/ /   _| |___  ___| /  \/ |__   ___  ___| | __
    |  __/ | | | / __|/ _ \ |   | '_ \ / _ \/ __| |/ /
    | |  | |_| | \__ \  __/ \__/\ | | |  __/ (__|   < 
    \_|   \__,_|_|___/\___|\____/_| |_|\___|\___|_|\_\
                                                  
                                                """)
    
print("--------------------------------------------------")


#program entry point is in the root directory of the project 
# file: pulsecheck.py will call this main function
# I did this so i didn't have to specify the file pathing's in every file 

def main():
    # May change name to something more descriptive in the future
    # This function is  CLI menu logic that handles user input and calls the appropriate functions
    # My goal is to keep things modular and organized, so I will keep the main function as is for now
    cli_menu_logic()


