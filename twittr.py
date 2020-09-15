import tweepy
from pathlib import Path


class Twittr:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        twitter_target_account: str,
        managed_tweets_file: Path,
        api_window_size: int,
    ):
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)
        self.cursor = tweepy.Cursor(self.api.user_timeline, id=twitter_target_account)
        self.managed_tweets_file = Path(managed_tweets_file)
        if not self.managed_tweets_file.exists():
            self.managed_tweets_file.touch()
        self.api_window_size = api_window_size

    def _get_managed_tweets_ids(self):
        self.managed_tweets_ids = self.managed_tweets_file.read_text().split()

    def _get_tweets_in_window(self):
        self.tweets_in_window = self.cursor.items(self.api_window_size)

    def _get_new_tweets(self):
        self._get_managed_tweets_ids()
        self._get_tweets_in_window()
        self.new_tweets = []
        for tweet in self.tweets_in_window:
            if tweet.id not in self.managed_tweets_ids:
                self.new_tweets.append(tweet)

    def update_managed_tweets_file(self):
        new_tweets_ids = [tweet.id for tweet in self.tweets_in_window]
        self.managed_tweets_file.write_text('\n'.join(new_tweets_ids))
