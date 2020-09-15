import tweepy
from prettyconf import config
from pathlib import Path

CONSUMER_KEY = config('TWITTER_API_KEY')
CONSUMER_SECRET = config('TWITTER_SECRET_KEY')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT')
WINDOW_SIZE = config('WINDOW_SIZE', cast=int)
MANAGED_TWEETS_FILE = config('MANAGED_TWEETS_FILE')

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)
cursor = tweepy.Cursor(api.user_timeline, id=TWITTER_TARGET_ACCOUNT)


def get_new_tweets():
    managed_tweets_file = Path(MANAGED_TWEETS_FILE)
    if not managed_tweets_file.exists():
        managed_tweets_file.touch()
    managed_tweets = managed_tweets_file.read_text().split()
    for tweet in cursor.items(WINDOW_SIZE):
        if tweet.id not in managed_tweets:
            yield tweet


for tweet in get_new_tweets():
    print(tweet.id)
