import tweepy
from prettyconf import config

CONSUMER_KEY = config('TWITTER_API_KEY')
CONSUMER_SECRET = config('TWITTER_SECRET_KEY')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT')
WINDOW_SIZE = config('WINDOW_SIZE', cast=int)

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)
cursor = tweepy.Cursor(api.user_timeline, id=TWITTER_TARGET_ACCOUNT)

for tweet in cursor.items(WINDOW_SIZE):
    print(tweet.id)
