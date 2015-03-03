import TweetParser
import TweetFetcher

tf = TweetFetcher()
tp = TweetParser()

tf.search()
tf.save(tf.tweet_list,'closing')

tp.delete_duplicates(tp.get_files_from_folder('./data'))

from_date = datetime.datetime(2015,2,25)
tp.find_relevant_tweets('./parsed/parsed_tweets.json',date=from_date)

