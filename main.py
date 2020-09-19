from prettyconf import config
from twittr import Twittr

CONSUMER_KEY = config('TWITTER_API_KEY')
CONSUMER_SECRET = config('TWITTER_SECRET_KEY')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT')
MANAGED_TWEETS_FILE = config('MANAGED_TWEETS_FILE')
API_WINDOW_SIZE = config('API_WINDOW_SIZE', cast=int)

t = Twittr(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TWITTER_TARGET_ACCOUNT,
    MANAGED_TWEETS_FILE,
    API_WINDOW_SIZE,
)
print(len(list(t.get_matching_tweets())))
t.update_managed_tweets_file()
