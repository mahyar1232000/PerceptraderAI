import logging
import tweepy  # نصب: pip install tweepy :contentReference[oaicite:8]{index=8}
import requests  # نصب: pip install requests :contentReference[oaicite:9]{index=9}
from sentiment.sentiment_analysis import SentimentAnalyzer


class SocialMediaAnalyzer:
    """
    تحلیل احساسات از منابع توییتر و StockTwits.
    """

    def __init__(self, twitter_credentials: dict, stocktwits_enabled: bool = True):
        # احراز هویت و ایجاد کلاینت توییتر
        self.twitter_api = self._authenticate_twitter(
            twitter_credentials)  # Tweepy OAuth1 :contentReference[oaicite:10]{index=10}
        self.sentiment_analyzer = SentimentAnalyzer()  # مثال: استفاده از SentimentAnalyzer
        self.stocktwits_enabled = stocktwits_enabled
        logging.info("SocialMediaAnalyzer initialized.")

    def _authenticate_twitter(self, credentials: dict) -> tweepy.API:
        """
        راه‌اندازی OAuth1 برای دسترسی به Twitter API v1.1
        """
        auth = tweepy.OAuth1UserHandler(
            credentials['api_key'],
            credentials['api_secret'],
            credentials['access_token'],
            credentials['access_token_secret']
        )
        logging.info("Twitter authentication successful.")
        return tweepy.API(auth, wait_on_rate_limit=True)  # limit handling :contentReference[oaicite:11]{index=11}

    def fetch_and_analyze_tweets(self, query: str, count: int = 100, lang: str = 'en') -> list[dict]:
        """
        جستجو در توییت‌ها بر اساس عبارت جستجو و تحلیل احساسات آن‌ها.
        :param query: عبارت جستجو (مثلاً دلار، طلا و …)
        :param count: تعداد توییت‌ها
        :param lang: زبان (مثلاً 'en')
        :return: لیستی از دیکشنری‌های نتایج تحلیل
        """
        tweets = self.twitter_api.search_tweets(q=query, count=count,
                                                lang=lang)  # Twitter search API :contentReference[oaicite:12]{index=12}
        results = []
        for tweet in tweets:
            analysis = self.sentiment_analyzer.analyze(tweet.text)
            analysis.update({
                'source': 'twitter',
                'id': tweet.id,
                'date': tweet.created_at
            })
            results.append(analysis)
        return results

    def fetch_and_analyze_stocktwits(self, symbol: str, count: int = 30) -> list[dict]:
        """
        دریافت پیام‌ها از StockTwits و تحلیل احساسات آن‌ها.
        :param symbol: نماد مالی (مثلاً 'AAPL' یا 'EURUSD')
        :param count: تعداد پیام‌ها (حداکثر 30 پیام مطابق محدودیت رایگان) :contentReference[oaicite:13]{index=13}
        :return: لیستی از دیکشنری‌های نتایج تحلیل
        """
        if not self.stocktwits_enabled:
            logging.warning("StockTwits integration disabled.")
            return []

        url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
        params = {'limit': count}
        results = []
        try:
            resp = requests.get(url, params=params,
                                timeout=10)  # Standard GET request :contentReference[oaicite:14]{index=14}
            data = resp.json()
            for msg in data.get('messages', []):
                text = msg.get('body', '')
                analysis = self.sentiment_analyzer.analyze(text)
                analysis.update({
                    'source': 'stocktwits',
                    'id': msg.get('id'),
                    'date': msg.get('created_at'),
                    'twits_sentiment': msg.get('entities', {}).get('sentiment', {}).get('basic')
                })
                results.append(analysis)
        except Exception as e:
            logging.error(f"StockTwits fetch error: {e}")
        return results
