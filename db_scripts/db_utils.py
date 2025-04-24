from db_config.db_test import get_connection
from db_config.db_test import get_connection
from datetime import datetime

def get_encounter_id_by_display_cd(display_cd):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT encounter_id FROM encounters WHERE encounter_display_cd = %s;", (display_cd,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    else:
        raise ValueError(f"Encounter with code {display_cd} not found.")
    


def save_feedback_to_db(encounter_id, feedback_data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Update the encounters table
        cursor.execute("""
            UPDATE encounters
            SET 
                feedback_text = %s,
                feedback_timestamp = %s,
                sentiment = %s,
                sentiment_score = %s
            WHERE encounter_id = %s;
        """, (
            feedback_data['feedback_text'],
            datetime.utcnow(),
            feedback_data['sentiment'],
            feedback_data['sentiment_score'],
            encounter_id
        ))

        # 2. Insert themes into feedback_themes table
        for theme in feedback_data['themes']:
            cursor.execute("""
                INSERT INTO feedback_themes (encounter_id, theme) VALUES (%s, %s);
            """, (encounter_id, theme))

        # 3. Insert mentioned providers into feedback_provider_mentions table
        for provider_name in feedback_data['mentioned_providers']:
            cursor.execute("""
                INSERT INTO feedback_provider_mentions (encounter_id, provider_name)
                VALUES (%s, %s);
            """, (encounter_id, provider_name))

        conn.commit()
        print(f"Feedback for encounter {encounter_id} and related data saved to DB.")

    except Exception as e:
        conn.rollback()
        print(f"Error saving feedback: {e}")

    finally:
        cursor.close()
        conn.close()
