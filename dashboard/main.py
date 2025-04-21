import json

    
def collect_feedback_from_encounter():
    
    with open('../data/encounters.json', 'r') as f:
     encounter = json.load(f)
     print(f"Loaded {len(encounter)} encounters.")



    for e in encounter:
        provider_names = [p['name'] for p in e['providers']]
        print(f"Encounter ID: {e['encounter_id']} | Patient: {e['patient_name']} | Unit: {e['unit']} | Providers: " + ", ".join(provider_names))

   
    ptInput = input("Please enter the encounter ID you would like to provide feedback for: ")
    # Check if input exists in the encounters
    encounter_found = False
    selected_encounter = None
    for e in encounter:
        if e['encounter_id'] == ptInput:
            encounter_found = True
            # Print the details of the selected encounter
            selected_encounter = e
            provider_names = [p['name'] for p in selected_encounter['providers']]
            # print(f"You have selected Encounter: {selected_encounter['encounter_id']} | Patient: {selected_encounter['patient_name']} | Unit: {selected_encounter['unit']} | Providers: " + ", ".join(provider_names))
            # ask for feedback for selected encounter.
            feedback = input("Please provide your feedback for this encounter: ")
            # Save feedback to the encounter
            selected_encounter['feedback'] = feedback
            # Save the updated encounters back to the file
            with open('../data/encounters.json', 'w') as f:
                json.dump(encounter, f, indent=4)
            print("Feedback saved successfully.")

            return {
                "encounter_id": selected_encounter['encounter_id'],
                "patient_name": selected_encounter['patient_name'],
                "unit": selected_encounter['unit'],
                "providers": provider_names,
                "feedback": feedback
            }
    if not encounter_found:
        print("Encounter ID not found, Please try again.")
        return collect_feedback_from_encounter()
collect_feedback_from_encounter()

