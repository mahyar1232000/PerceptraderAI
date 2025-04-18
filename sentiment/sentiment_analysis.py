import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """
    تحلیل احساسات متن با استفاده از VADER (Valence Aware Dictionary and sEntiment Reasoner).
    """

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()  # نصب: pip install vaderSentiment :contentReference[oaicite:4]{index=4}
        logging.info("SentimentAnalyzer initialized.")  # لاگ راه‌اندازی

    def analyze(self, text: str) -> dict:
        """
        تحلیل احساسات متن ورودی و بازگشت دیکشنری شامل متن، برچسب و امتیازات ترکیبی.
        :param text: متن ورودی برای تحلیل
        :return: {'text': str, 'sentiment': str, 'score': dict}
        """
        # محاسبه امتیازهای احساسی
        score = self.analyzer.polarity_scores(text)  # VADER polarity_scores API :contentReference[oaicite:5]{index=5}
        compound = score['compound']  # نمرهٔ ترکیبی
        sentiment = self._interpret_score(compound)  # تفسیر نمره
        logging.debug(f"Text: {text} | Sentiment: {sentiment} | Score: {score}")
        return {
            'text': text,
            'sentiment': sentiment,
            'score': score
        }

    @staticmethod
    def _interpret_score(compound_score: float) -> str:
        """
        تفسیر نمرهٔ ترکیبی به سه برچسب 'positive', 'neutral', 'negative'.
        :param compound_score: نمرهٔ ترکیبی از -1.0 تا +1.0
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
