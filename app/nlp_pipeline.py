from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import json

#load thememes from json file

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
with open('app/themes.json', 'r') as f:
    theme_keywords = json.load(f)

def detect_themes(text, theme_keywords):
    matched_themes = []
    text_lower = text.lower()
    for theme, keywords in theme_keywords.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                matched_themes.append(theme)
                break  # Stop after first match per theme
    return matched_themes

def detect_mentioned_providers(feedback_text, providers):
    mentioned = []
    text_lower = feedback_text.lower()
    for provider in providers:
        provider_name = provider['name'].lower()
        if provider_name in text_lower:
            mentioned.append(provider['name'])
    return mentioned

def analyze_feedback(text):
    scores = sia.polarity_scores(text)
    compound = scores['compound']  # ranges from -1.0 to +1.0

    sentiment = (
        "positive" if compound > 0.05 else
        "negative" if compound < -0.05 else
        "neutral"
    )

    themes = detect_themes(text, theme_keywords)

    return {
        "sentiment": sentiment,
        "sentiment_score": compound,
        "themes": themes  # Themes only, no provider detection here
    }



# Example test
if __name__ == "__main__":
    test_texts = [  
        "Loved it, Dr. Smith was great!",
        "This wasn't my favorite visit, Dr. Reyes was rude and dismissive.",
        "Everything was okay.",
        "Terrible service, but the nurse was helpful."
    ]

    for text in test_texts:
        result = analyze_feedback(text)
        print(f"Text: {text}")
        print(f"Sentiment: {result['sentiment']}, Score: {result['sentiment_score']}")
        print(f"Mentioned Providers: {result.get('mentioned_providers', [])}")
        print(f"Themes: {result['themes']}")
        print("----")
