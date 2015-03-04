from tweetparser import TweetParser
from tweetfetcher import TweetFetcher
import datetime
tf = TweetFetcher()
tp = TweetParser()

date = datetime.datetime(2015,3,1)


tf.search(until=date)

tf.save(tf.tweet_list,'closing')

tp.delete_duplicates(tp.get_files_from_folder('./data'))

from_date = datetime.datetime(2015,2,25)
tp.find_relevant_tweets('./parsed/parsed_tweets.json',date=from_date)

