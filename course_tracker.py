from pathlib import Path

import tweepy
from logzero import logger

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
        last_managed_tweet_file: Path,
        api_window_size: int,
        search_terms_file: Path,
    ):
        logger.info('Building Tweepy API handler...')
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)
        self.twitter_target_account = twitter_target_account

        self.last_managed_tweet_file = Path(last_managed_tweet_file)
        if not self.last_managed_tweet_file.exists():
            logger.warning('File of last managed tweet not found. Creating...')
            self.last_managed_tweet_file.touch()

        self.api_window_size = api_window_size
        self.api_tweets = []

        self.search_terms_file = Path(search_terms_file)
        if not self.search_terms_file.exists():
            logger.warning('File of search terms not found. Creating...')
            self.search_terms_file.touch()

    def get_last_managed_tweet_id(self):
        try:
            return int(self.last_managed_tweet_file.read_text().strip())
        except ValueError:
            return 1

    def get_new_tweets(self, force_api_call=False):
        # avoid not needed API calls
        if not self.api_tweets or force_api_call:
            logger.info('Getting tweets from API...')
            cursor = tweepy.Cursor(
                self.api.user_timeline,
                id=self.twitter_target_account,
                tweet_mode='extended',
                since_id=self.get_last_managed_tweet_id(),
            )
            self.api_tweets = list(cursor.items(self.api_window_size))
        return self.api_tweets

    def get_search_terms(self):
        yield from self.search_terms_file.read_text().split()

    def get_matching_tweets(self):
        logger.info('Getting matching tweets from search terms...')
        regex = utils.get_compiled_regex(tuple(self.get_search_terms()))
        for tweet in self.get_new_tweets():
            if regex.search(tweet.full_text) is not None:
                yield tweet

    def update_last_managed_tweet_file(self):
        logger.info('Updating last managed tweet on file...')
        if managed_tweets_ids := [tweet.id for tweet in self.get_new_tweets()]:
            self.last_managed_tweet_file.write_text(str(max(managed_tweets_ids)))

    def get_couponed_course_tracker_urls(self):
        logger.info('Getting tracker url of free couponed courses..')
        for tweet in self.get_matching_tweets():
            ct_tweet = CT_Tweet(tweet)
            if ct_tweet.is_couponed():
                yield ct_tweet.get_course_tracker_url()
