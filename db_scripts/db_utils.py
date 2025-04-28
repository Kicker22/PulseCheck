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
    


from db_config.db_test import get_connection
from datetime import datetime

def save_feedback_to_db(encounter_id, feedback_data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Insert feedback and get feedback_id
        cursor.execute("""
            INSERT INTO feedback (encounter_id, feedback_text, feedback_timestamp, sentiment, sentiment_score)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING feedback_id;
        """, (
            encounter_id,
            feedback_data['feedback_text'],
            datetime.utcnow(),
            feedback_data['sentiment'],
            feedback_data['sentiment_score']
        ))

        feedback_id = cursor.fetchone()[0]
        print(f"DEBUG: Feedback ID {feedback_id} created.")

        # 2. Insert themes into feedback_themes
        for theme in feedback_data['themes']:
            cursor.execute("""
                INSERT INTO feedback_themes (feedback_id, theme)
                VALUES (%s, %s);
            """, (feedback_id, theme))

        print(f"DEBUG: Saved {len(feedback_data['themes'])} themes.")

        # 3. Insert mentioned providers into feedback_providers
        for provider in feedback_data['mentioned_providers']:
            cursor.execute("""
                INSERT INTO feedback_provider_mentions (feedback_id, provider_id)
                VALUES (%s, %s);
            """, (feedback_id, provider['provider_id']))

        print(f"DEBUG: Saved {len(feedback_data['mentioned_providers'])} mentioned providers.")

        conn.commit()
        print(f"Feedback for encounter {encounter_id} fully saved to DB.")

    except Exception as e:
        conn.rollback()
        print(f"Error saving feedback: {e}")
    finally:
        cursor.close()
        conn.close()

