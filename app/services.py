from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_sentiment_scores(text):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)