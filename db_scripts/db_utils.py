from db_config.db_test import get_connection
from datetime import datetime

def get_encounter_id_by_display_cd(display_cd):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT encounter_id FROM encounters WHERE encounter_display_cd = %s;", (display_cd,))
                result = cursor.fetchone()

        if result:
            return result[0]
        else:
            raise ValueError(f"Encounter with code {display_cd} not found.")
    except Exception as e:
        print(f"Error retrieving encounter ID: {e}")
        raise
from db_config.db_test import get_connection

def fetch_providers_for_encounter(encounter_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT p.provider_id, p.name, p.role
                    FROM providers p
                    JOIN encounter_providers ep ON p.provider_id = ep.provider_id
                    WHERE ep.encounter_id = %s;
                """, (encounter_id,))
                rows = cursor.fetchall()

        providers = []
        for row in rows:
            provider_id, name, role = row
            providers.append({
                'provider_id': provider_id,
                'name': name,
                'role': role
            })

        return providers

    except Exception as e:
        print(f"Error fetching providers for encounter {encounter_id}: {e}")
        return []

def fetch_feedback_for_encounter(encounter_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        f.feedback_text,
                        f.sentiment,
                        f.sentiment_score, 
                        COALESCE(STRING_AGG(DISTINCT t.name, ', '), '') AS themes,
                        COALESCE(STRING_AGG(DISTINCT p.name, ', '), '') AS mentioned_providers
                    FROM feedback f
                    LEFT JOIN feedback_themes ft ON f.id = ft.feedback_id
                    LEFT JOIN themes t ON ft.theme_id = t.theme_id
                    LEFT JOIN feedback_mentions fm ON f.id = fm.feedback_id
                    LEFT JOIN providers p ON fm.provider_id = p.provider_id
                    WHERE f.encounter_id = %s
                    GROUP BY f.id, f.feedback_text, f.sentiment, f.sentiment_score;
                """, (encounter_id,))
                row = cursor.fetchone()

        if row:
            feedback_text, sentiment, sentiment_score, themes, mentioned_providers = row
            return {
                "feedback_text": feedback_text,
                "sentiment": sentiment,
                "sentiment_score": float(sentiment_score),
                "themes": themes.split(', ') if themes else [],
                "mentioned_providers": mentioned_providers.split(', ') if mentioned_providers else []
            }
        else:
            return None

    except Exception as e:
        print(f"Error fetching feedback for encounter {encounter_id}: {e}")
        return None

def fetch_encounter_details(encounter_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.encounter_id,
                        e.unit,
                        e.encounter_display_cd,
                        e.admission_timestamp,
                        e.discharge_timestamp,
                        ARRAY_AGG(DISTINCT p.name) AS provider_names
                    FROM encounters e
                    LEFT JOIN encounter_providers ep ON e.encounter_id = ep.encounter_id
                    LEFT JOIN providers p ON ep.provider_id = p.provider_id
                    WHERE e.encounter_id = %s
                    GROUP BY e.encounter_id, e.unit, e.encounter_display_cd, e.admission_timestamp, e.discharge_timestamp;
                """, (encounter_id,))
                row = cursor.fetchone()

        if row:
            return {
                "encounter_id": row[0],
                "unit": row[1],
                "encounter_display_cd": row[2],
                "admission_timestamp": row[3],
                "discharge_timestamp": row[4],
                "providers": row[5]
            }
        else:
            return None

    except Exception as e:
        print(f"Error fetching encounter details for {encounter_id}: {e}")
        return None


def fetch_all_providers():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT provider_id, name, role
                    FROM providers;
                """)
                rows = cursor.fetchall()

        providers = []
        for row in rows:
            provider_id, name, role = row
            providers.append({
                'provider_id': provider_id,
                'name': name,
                'role': role,
            })

        return providers

    except Exception as e:
        print(f"Error fetching providers: {e}")
        return []

def fetch_theme_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT t.name, COUNT(*) AS count
                    FROM feedback_themes ft
                    JOIN themes t ON ft.theme_id = t.theme_id
                    GROUP BY t.name
                    ORDER BY count DESC;
                """)
                rows = cursor.fetchall()

        themes = []
        for row in rows:
            theme_name, count = row
            themes.append({
                'theme': theme_name,
                'count': count
            })

        return themes

    except Exception as e:
        print(f"Error fetching theme summary: {e}")
        return []

def fetch_provider_themes_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.name AS provider_name,
                        t.name AS theme,
                        AVG(f.sentiment_score) AS avg_sentiment
                    FROM providers p
                    JOIN feedback_mentions fm ON p.provider_id = fm.provider_id
                    JOIN feedback f ON fm.feedback_id = f.id
                    JOIN feedback_themes ft ON f.id = ft.feedback_id
                    JOIN themes t ON ft.theme_id = t.theme_id
                    GROUP BY p.name, t.name
                    ORDER BY p.name, t.name;
                """)
                rows = cursor.fetchall()

        provider_dict = {}
        for provider_name, theme, avg_sentiment in rows:
            score = round(float(avg_sentiment), 4) if avg_sentiment else 0.0
            if score > 0.75:
                sentiment_label = "very positive"
            elif 0.25 < score <= 0.75:
                sentiment_label = "positive"
            elif -0.25 <= score <= 0.25:
                sentiment_label = "neutral"
            elif -0.75 <= score < -0.25:
                sentiment_label = "negative"
            else:
                sentiment_label = "very negative"

            if provider_name not in provider_dict:
                provider_dict[provider_name] = []

            provider_dict[provider_name].append({
                'theme': theme,
                'sentiment_score': score,
                'sentiment_label': sentiment_label
            })

        return [
            {'provider_name': name, 'themes': themes}
            for name, themes in provider_dict.items()
        ]

    except Exception as e:
        print(f"Error fetching nested provider themes: {e}")
        return []
    
def fetch_admin_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        COUNT(*) AS total_feedback,
                        ROUND(AVG(sentiment_score)::NUMERIC, 4) AS average_sentiment,
                        MAX(feedback_timestamp) AS most_recent_feedback
                    FROM feedback;
                """)
                row = cursor.fetchone()

        return {
            "total_feedback": row[0],
            "average_sentiment": float(row[1]) if row[1] is not None else 0.0,
            "most_recent_feedback": row[2].isoformat() if row[2] else None
        }

    except Exception as e:
        print(f"Error fetching admin summary: {e}")
        return {
            "total_feedback": 0,
            "average_sentiment": 0.0,
            "most_recent_feedback": None
        }

def fetch_theme_summary_for_admin():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        t.name,
                        COUNT(*) AS count,
                        ROUND(AVG(f.sentiment_score)::NUMERIC, 4) AS avg_sentiment
                    FROM feedback_themes ft
                    JOIN themes t ON ft.theme_id = t.theme_id
                    JOIN feedback f ON ft.feedback_id = f.id
                    GROUP BY t.name
                    ORDER BY count DESC;
                """)
                rows = cursor.fetchall()

        return [
            {
                "theme": row[0],
                "count": row[1],
                "average_sentiment": float(row[2]) if row[2] is not None else 0.0
            }
            for row in rows
        ]

    except Exception as e:
        print(f"Error fetching theme summary: {e}")
        return []

def fetch_unit_performance():  
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.unit,
                        COUNT(f.id) AS feedback_count,
                        ROUND(AVG(f.sentiment_score)::NUMERIC, 4) AS average_sentiment,
                        MODE() WITHIN GROUP (ORDER BY f.sentiment) AS dominant_sentiment
                    FROM feedback f
                    JOIN encounters e ON f.encounter_id = e.encounter_id
                    GROUP BY e.unit
                    ORDER BY e.unit;
                """)
                rows = cursor.fetchall()

        return [
            {
                "unit": unit,
                "feedback_count": count,
                "average_sentiment": float(avg_sentiment) if avg_sentiment is not None else 0.0,
                "sentiment_label": dominant_sentiment if dominant_sentiment else "neutral"
            }
            for unit, count, avg_sentiment, dominant_sentiment in rows
        ]

    except Exception as e:
        print(f"Error fetching unit performance: {e}")
        return []

def fetch_sentiment_over_time():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Daily sentiment summary
                cursor.execute("""
                    SELECT 
                        DATE(feedback_timestamp) AS feedback_date,
                        COUNT(id) AS feedback_count,
                        ROUND(AVG(sentiment_score)::NUMERIC, 4) AS average_sentiment
                    FROM feedback
                    GROUP BY feedback_date
                    ORDER BY feedback_date;
                """)
                day_rows = cursor.fetchall()

                # Date range and total count
                cursor.execute("""
                    SELECT 
                        MIN(DATE(feedback_timestamp)),
                        MAX(DATE(feedback_timestamp)),
                        COUNT(id)
                    FROM feedback;
                """)
                start_date, end_date, total_feedback_count = cursor.fetchone()

        return {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "total_feedback_count": total_feedback_count,
            "days": [
                {
                    "date": row[0].isoformat(),
                    "feedback_count": row[1],
                    "average_sentiment": float(row[2]) if row[2] is not None else 0.0
                }
                for row in day_rows
            ]
        }

    except Exception as e:
        print(f"Error fetching sentiment over time: {e}")
        return {
            "start_date": None,
            "end_date": None,
            "total_feedback_count": 0,
            "days": []
        }

def save_feedback_to_db(encounter_id, feedback_data):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. Insert feedback and get feedback ID
                cursor.execute("""
                    INSERT INTO feedback (encounter_id, feedback_text, feedback_timestamp, sentiment, sentiment_score)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
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

                # 3. Insert mentioned providers into feedback_mentions
                for provider in feedback_data['mentioned_providers']:
                    if not isinstance(provider, dict) or 'provider_id' not in provider:
                        raise ValueError(f"Invalid provider format: {provider}")
                    print("DEBUG: Saving provider mention:", provider)
                    cursor.execute("""
                        INSERT INTO feedback_mentions (feedback_id, provider_id)
                        VALUES (%s, %s);
                    """, (feedback_id, provider['provider_id']))

                print(f"DEBUG: Saved {len(feedback_data['mentioned_providers'])} mentioned providers.")

            conn.commit()
            print(f"Feedback for encounter {encounter_id} fully saved to DB.")

    except Exception as e:
        print(f"Error saving feedback: {e}")
        raise
