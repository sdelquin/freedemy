from prettyconf import config
from twittr import Twittr

CONSUMER_KEY = config('TWITTER_API_KEY')
CONSUMER_SECRET = config('TWITTER_SECRET_KEY')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT')
MANAGED_TWEETS_FILE = config('MANAGED_TWEETS_FILE')
API_WINDOW_SIZE = config('API_WINDOW_SIZE', cast=int)
MATCHING_RULES_FILE = config('MATCHING_RULES_FILE')

t = Twittr(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TWITTER_TARGET_ACCOUNT,
    MANAGED_TWEETS_FILE,
    API_WINDOW_SIZE,
    MATCHING_RULES_FILE,
)

for tweet in t.get_matching_tweets():
    print(tweet.text)
t.update_managed_tweets_file()
