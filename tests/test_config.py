from prettyconf import config

CONFIG_KEYS = (
    'TWITTER_API_KEY',
    'TWITTER_SECRET_KEY',
    'TWITTER_TARGET_ACCOUNT',
    'LAST_MANAGED_TWEET_FILE',
    'API_WINDOW_SIZE',
    'SEARCH_TERMS_FILE',
    'SLACK_API_TOKEN',
    'SLACK_CHANNEL',
)


def test_get_configs():
    for key in CONFIG_KEYS:
        assert config(key) != ''