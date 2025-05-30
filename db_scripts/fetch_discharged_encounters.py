from collections import defaultdict
from db_config.db_test import get_connection

def fetch_discharged_encounters():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT 
                    e.encounter_id,
                    e.patient_name,
                    e.unit,
                    p.provider_id,
                    p.name AS provider_name,
                    p.role AS provider_role
                FROM encounters e
                JOIN encounter_providers ep ON e.encounter_id = ep.encounter_id
                JOIN providers p ON ep.provider_id = p.provider_id
                LEFT JOIN feedback f ON e.encounter_id = f.encounter_id
                WHERE e.discharged = TRUE
                AND e.declined = FALSE
                AND f.id IS NULL
                """

                cursor.execute(query)
                rows = cursor.fetchall()

        # Group providers under each encounter
        encounters = defaultdict(lambda: {
            "patient_name": "",
            "unit": "",
            "providers": [],
            "formatted_id": ""
        })

        for row in rows:
            encounter_id, patient_name, unit, provider_id, provider_name, provider_role = row
            formatted_id = encounter_id  # encounter_id is already 'E001' format

            encounters[formatted_id]["patient_name"] = patient_name
            encounters[formatted_id]["unit"] = unit
            encounters[formatted_id]["formatted_id"] = formatted_id
            encounters[formatted_id]["providers"].append({
                "provider_id": provider_id,
                "name": provider_name,
                "role": provider_role
            })

        return dict(encounters)

    except Exception as e:
        print(f"Error fetching discharged encounters: {e}")
        raise
