from db_scripts.fetch_discharged_encounters import fetch_discharged_encounters

def display_encounters():
    encounters = fetch_discharged_encounters()

    if not encounters:
        print("No discharged encounters available for feedback.")
        return None

    print("\nAvailable Encounters for Feedback:")
    print("--------------------------------------------------")

    for eid, data in encounters.items():
        providers = ", ".join(f"{p['name']} ({p['role']})" for p in data['providers'])
        print(f"Encounter ID: {eid} | Patient: {data['patient_name']} | Unit: {data['unit']} | Providers: {providers}")

    return encounters  # Optional: return for further use
