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
                    SELECT p.id, p.name, p.role
                    FROM providers p
                    JOIN encounter_providers ep ON p.id = ep.provider_id
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
                    SELECT f.feedback_text, f.sentiment, f.sentiment_score, 
                           STRING_AGG(DISTINCT t.theme, ', ') AS themes,
                           STRING_AGG(DISTINCT p.name, ', ') AS mentioned_providers
                    FROM feedback f
                    LEFT JOIN feedback_themes t ON f.id = t.feedback_id
                    LEFT JOIN feedback_provider_mentions fp ON f.id = fp.feedback_id
                    LEFT JOIN providers p ON fp.provider_id = p.id
                    WHERE f.encounter_id = %s
                    GROUP BY f.feedback_text, f.sentiment, f.sentiment_score;
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

def fetch_all_providers():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, name, role, provider_code
                    FROM providers;
                """)
                rows = cursor.fetchall()

        providers = []
        for row in rows:
            provider_id, name, role, provider_code = row
            providers.append({
                'provider_id': provider_id,
                'name': name,
                'role': role,
                'provider_code': provider_code
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
                    SELECT theme, COUNT(*) AS count
                    FROM feedback_themes
                    GROUP BY theme
                    ORDER BY count DESC;
                """)
                rows = cursor.fetchall()

        themes = []
        for row in rows:
            theme, count = row
            themes.append({
                'theme': theme,
                'count': count
            })

        return themes

    except Exception as e:
        print(f"Error fetching theme summary: {e}")
        return []

def fetch_provider_stats():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT p.name, p.role, COUNT(fp.feedback_id) AS feedback_count, 
                           AVG(f.sentiment_score) AS avg_sentiment
                    FROM providers p
                    LEFT JOIN feedback_provider_mentions fp ON p.id = fp.provider_id
                    LEFT JOIN feedback f ON fp.feedback_id = f.id
                    GROUP BY p.name, p.role
                    ORDER BY feedback_count DESC;
                """)
                rows = cursor.fetchall()

        stats = []
        for row in rows:
            name, role, feedback_count, avg_sentiment = row
            stats.append({
                'provider_name': name,
                'role': role,
                'feedback_count': feedback_count,
                'avg_sentiment_score': round(float(avg_sentiment), 4) if avg_sentiment else None
            })

        return stats

    except Exception as e:
        print(f"Error fetching provider stats: {e}")
        return []

def fetch_provider_themes_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.name AS provider_name,
                        t.theme,
                        AVG(f.sentiment_score) AS avg_sentiment
                    FROM providers p
                    JOIN feedback_provider_mentions fp ON p.id = fp.provider_id
                    JOIN feedback f ON fp.feedback_id = f.id
                    JOIN feedback_themes t ON f.id = t.feedback_id
                    GROUP BY p.name, t.theme
                    ORDER BY p.name, t.theme;
                """)
                rows = cursor.fetchall()

        provider_dict = {}
        for row in rows:
            provider_name, theme, avg_sentiment = row
            score = round(float(avg_sentiment), 4) if avg_sentiment else 0.0
            # Refined sentiment label logic
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

        result = []
        for provider_name, themes in provider_dict.items():
            result.append({
                'provider_name': provider_name,
                'themes': themes
            })

        return result

    except Exception as e:
        print(f"Error fetching nested provider themes: {e}")
        return []



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

                # 3. Insert mentioned providers into feedback_provider_mentions
                for provider in feedback_data['mentioned_providers']:
                    if not isinstance(provider, dict) or 'provider_id' not in provider:
                        raise ValueError(f"Invalid provider format: {provider}")
                    print("DEBUG: Saving provider mention:", provider)
                    cursor.execute("""
                        INSERT INTO feedback_provider_mentions (feedback_id, provider_id)
                        VALUES (%s, %s);
                    """, (feedback_id, provider['provider_id']))

                print(f"DEBUG: Saved {len(feedback_data['mentioned_providers'])} mentioned providers.")

            conn.commit()
            print(f"Feedback for encounter {encounter_id} fully saved to DB.")

    except Exception as e:
        print(f"Error saving feedback: {e}")
        raise
