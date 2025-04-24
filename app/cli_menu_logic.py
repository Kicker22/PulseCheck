from app.feedback_handler import handle_feedback, user_wants_to_proceed, handle_declined_feedback
from app.killSwitch import killSwitch
from app.display_encounters import display_encounters
from db_scripts.db_utils import get_encounter_id_by_display_cd



def cli_menu_logic():
    try:
        while True:
            print("\nPulseCheck Menu\n")
            print("1. Leave feedback")
            print("2. Exit PulseCheck")
            choice = input("\nChoose an option (1-2): ").strip()
            print("\n--------------------------------------------------")

            if choice == "1":
                try:
                    # Display encounters and get feedback
                    display_encounters()
                    display_cd = input("\nEnter the Encounter ID you would like to provide feedback for: ").strip().upper()

                    killSwitch(display_cd)  # Check if user wants to exit

                    #convert display_cd to encounter_id
                    encounter_id = get_encounter_id_by_display_cd(display_cd)

                    if user_wants_to_proceed(display_cd):
                        feedback_text = input("Please provide your feedback: ").strip()
                        feedback_entry = handle_feedback(encounter_id, feedback_text)
                        print(f"\nFeedback saved for encounter {encounter_id}.")
                        print("Feedback Summary:")
                        print(f"Feedback Entry: {feedback_entry}")
                    else:
                        handle_declined_feedback(encounter_id)
                except ValueError as e:
                    print(f"Error: {e}")
            elif choice == "2":
                killSwitch(choice)  # Call the killSwitch function to exit
            else:
                print("Invalid choice. Try again.")
    except Exception as e:
        print(f"An error occurred: {e}")