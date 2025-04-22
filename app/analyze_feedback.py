import json
from textblob import TextBlob
from app.config import THEMES_PATH  # path to your themes.json
# THEMES_PATH = "../data/themes.json"
def analyze_feedback(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    sentiment = (
        "positive" if polarity > 0 else
        "negative" if polarity < 0 else
        "neutral"
    )

    # Load themes
    with open(THEMES_PATH, 'r') as f:
        themes_data = json.load(f)

    detected_themes = []
    text_lower = text.lower()

    for theme, keywords in themes_data.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                detected_themes.append(theme)
                break  # Avoid duplicate theme entries

    return {
        "sentiment": sentiment,
        "sentiment_score": polarity,
        "themes": detected_themes
    }

# Example usage
# This part is for testing the function independently. You can remove it when integrating into your application.
if __name__ == "__main__":
    sample_text = "The staff was friendly but I had to wait a long time."
    result = analyze_feedback(sample_text)
    print("Analysis Result:")
    print(result)
