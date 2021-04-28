from pathlib import Path

import tweepy
from logzero import logger

import settings
import utils


class CT_Tweet:
    ''' Course Tracker Tweet '''

    def __init__(self, tweet: tweepy.models.Status, course_tracker_base_url):
        self.tweet = tweet
        self.course_tracker_base_url = course_tracker_base_url

    def get_course_tracker_url(self):
        for url in self.tweet.entities['urls']:
            if url['expanded_url'].startswith(self.course_tracker_base_url):
                return url['expanded_url']
        logger.error('Unable to locate course tracker url')


class CT_Twitter:
    ''' Course Tracker Twitter '''

    def __init__(
        self,
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_SECRET_KEY,
        course_tracker_twitter=settings.COURSE_TRACKER_TWITTER,
        course_tracker_base_url=settings.COURSE_TRACKER_BASE_URL,
        last_managed_tweet_file=settings.LAST_MANAGED_TWEET_FILE,
        api_window_size=settings.TWITTER_API_WINDOW_SIZE,
        search_terms_file=settings.SEARCH_TERMS_FILE,
    ):
        logger.info('Building Tweepy API handler...')
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)
        self.course_tracker_twitter = course_tracker_twitter
        self.course_tracker_base_url = course_tracker_base_url

        self.last_managed_tweet_file = Path(last_managed_tweet_file)
        if not self.last_managed_tweet_file.exists():
            logger.warning('File of last managed tweet not found. Creating...')
            self.last_managed_tweet_file.touch()

        self.api_window_size = api_window_size
        self.api_tweets = None

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
        if self.api_tweets is None or force_api_call:
            logger.info('Getting new tweets from API...')
            cursor = tweepy.Cursor(
                self.api.user_timeline,
                id=self.course_tracker_twitter,
                tweet_mode='extended',
                since_id=self.get_last_managed_tweet_id(),
            )
            self.api_tweets = list(cursor.items(self.api_window_size))
        return self.api_tweets

    def get_search_terms(self):
        yield from self.search_terms_file.read_text().strip().split('\n')

    def get_matching_tweets(self):
        logger.info('Starting tweet matching from search terms...')
        regex = utils.get_compiled_regex(tuple(self.get_search_terms()))
        for tweet in self.get_new_tweets():
            logger.debug(f'\n{tweet.full_text}')
            if regex.search(tweet.full_text) is not None:
                yield tweet
            else:
                logger.info('Tweet not matching search terms...')

    def update_last_managed_tweet_file(self):
        logger.info('Updating last managed tweet on file...')
        if managed_tweets_ids := [tweet.id for tweet in self.get_new_tweets()]:
            self.last_managed_tweet_file.write_text(str(max(managed_tweets_ids)))

    def get_course_tracker_urls(self):
        logger.info('Getting tracker url of courses...')
        for tweet in self.get_matching_tweets():
            ct_tweet = CT_Tweet(tweet, self.course_tracker_base_url)
            yield ct_tweet.get_course_tracker_url()
