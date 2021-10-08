from nltk.sentiment.vader import SentimentIntensityAnalyzer
from underthesea import sentiment
from langdetect import detect


class Scores:
    def __init__(self):
        self.positive = 0
        self.negative = 0


def analyze(overviews, scores):
    sia = SentimentIntensityAnalyzer()
    for overview in overviews:
        if detect(overview[0]) == "vi":
            result = sentiment(overview)
            if result == "positive":
                scores.positive += 1
            elif result == "negative":
                scores.negative += 1
        else:
            ps = sia.polarity_scores(overview[0])
            if ps["pos"] > ps["neg"]:
                scores.positive += 1
            elif ps["pos"] < ps["neg"]:
                scores.negative += 1
