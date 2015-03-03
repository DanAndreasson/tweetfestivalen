import TweetParser
import TweetFetcher

tf = TweetFetcher()
tp = TweetParser()

tf.search()
tf.save(tf.tweet_list,'closing')

tp.delete_duplicates(tp.get_files_from_folder('./data'))

