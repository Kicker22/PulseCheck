from app.display_feedback_candidates import display_candidates
from app.feedback_handler import handle_feedback, user_wants_to_proceed, handle_declined_feedback
from app.killSwitch import killSwitch
from app.discharge_admit_handler import discharge_patient, admit_patient
from app.handle_user_input import handle_user_input

def cli_menu_logic():
    try:
        while True:
            print("\nPulseCheck Menu\n")
            print("1. Leave feedback")
            print("2. Discharge a patient")
            print("3. Admit a patient")
            print("4. Exit program")
            choice = input("\nChoose an option (1-4): ").strip()
            print("\n--------------------------------------------------")

            if choice == "1":
                try:
                    # Display encounters and get feedback
                    display_candidates()
                    encounter_id = input("\nEnter the Encounter ID you would like to provide feedback for: ").strip().upper()
                    killSwitch(encounter_id)  # Check if user wants to exit
                    if user_wants_to_proceed(encounter_id):
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
                # use killswitch to check if user wants to exit
                discharge_patient()
            elif choice == "3":
                admit_patient()
            elif choice == "4":
                killSwitch(choice)  # Call the killSwitch function to exit
            else:
                print("Invalid choice. Try again.")
    except Exception as e:
        print(f"An error occurred: {e}")