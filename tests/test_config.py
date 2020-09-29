from prettyconf import config

CONFIG_KEYS = (
    'TWITTER_API_KEY',
    'TWITTER_SECRET_KEY',
    'TWITTER_TARGET_ACCOUNT',
    'SLACK_API_TOKEN',
    'SLACK_CHANNEL',
)


def test_get_configs():
    for key in CONFIG_KEYS:
        assert config(key) != ''
