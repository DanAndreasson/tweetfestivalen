from tweetparser import TweetParser
from tweetfetcher import TweetFetcher
from random import randint
import datetime
import os

def makedirs(folder):
    os.mkdir('./data/' +folder)
    os.mkdir('./parsed/' +folder)

folder = str(randint(100000,999999))
makedirs(folder)
tf = TweetFetcher()
tp = TweetParser()

date = datetime.datetime(2015,3,4)

tf.search(folder,until=date)
tf.save(tf.tweet_list,'closing',folder)

tp.delete_duplicates(tp.get_files_from_folder('./data/'+folder),folder)

from_date = datetime.datetime(2015,2,25)
tp.find_relevant_tweets('./parsed/'+folder+'/parsed_tweets.json',date=from_date)


os.system('python3 main.py train '+folder)
os.system('python3 main.py evaluate '+folder+' ./parsed/'+folder+'/parsed_tweets.json')
