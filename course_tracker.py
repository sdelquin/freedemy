from pathlib import Path

import tweepy

import utils


class CT_Tweet:
    ''' Course Tracker Tweet '''

    def __init__(self, tweet: tweepy.models.Status):
        self.tweet = tweet

    def is_couponed(self):
        hashtags = [h['text'].upper() for h in self.tweet.entities['hashtags']]
        return 'COUPON' in hashtags

    def get_course_tracker_url(self):
        return self.tweet.entities['urls'][0]['expanded_url']


class CT_Twitter:
    ''' Course Tracker Twitter '''

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        twitter_target_account: str,
        managed_tweets_file: Path,
        api_window_size: int,
        matching_rules_file: Path,
    ):
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)
        self.cursor = tweepy.Cursor(
            self.api.user_timeline, id=twitter_target_account, tweet_mode='extended'
        )

        self.managed_tweets_file = Path(managed_tweets_file)
        if not self.managed_tweets_file.exists():
            self.managed_tweets_file.touch()

        self.api_window_size = api_window_size
        self.api_tweets = []

        self.matching_rules_file = Path(matching_rules_file)
        if not self.matching_rules_file.exists():
            self.matching_rules_file.touch()

    def get_managed_tweets_ids(self):
        yield from [
            int(tweet_id) for tweet_id in self.managed_tweets_file.read_text().split()
        ]

    def get_api_tweets(self, force_api_call=False):
        # avoid not needed API calls
        if not self.api_tweets or force_api_call:
            self.api_tweets = list(self.cursor.items(self.api_window_size))
        return self.api_tweets

    def get_new_tweets(self):
        for tweet in self.get_api_tweets():
            if tweet.id not in list(self.get_managed_tweets_ids()):
                yield tweet

    def get_maching_rules(self):
        yield from self.matching_rules_file.read_text().split()

    def get_matching_tweets(self):
        regex = utils.get_compiled_regex(tuple(self.get_maching_rules()))
        for tweet in self.get_new_tweets():
            if regex.search(tweet.full_text) is not None:
                yield tweet

    def update_managed_tweets_file(self):
        api_tweets_ids = [str(tweet.id) for tweet in self.get_api_tweets()]
        self.managed_tweets_file.write_text('\n'.join(api_tweets_ids))

    def get_couponed_course_tracker_urls(self):
        for tweet in self.get_matching_tweets():
            ct_tweet = CT_Tweet(tweet)
            if ct_tweet.is_couponed():
                yield ct_tweet.get_course_tracker_url()