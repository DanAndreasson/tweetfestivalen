from os import listdir
import json
from os.path import isfile, join

class TweetParser:

  def __init__(self):
    pass
  
  def delete_duplicates(self,files):
    """ Parse go though all ids of all tweets and delete duplicates for all
    files"""
    all_tweets = []
    total_tweets = 0
    tweet_ids = []
    for f in files:
      with open(f, 'r') as read_file:
        obj = json.load(read_file)
        for tweet in obj:
          total_tweets += 1
          if tweet["id"] not in tweet_ids:
            all_tweets.append(tweet)
            tweet_ids.append(tweet["id"])
    print("Total Tweets: " + str(total_tweets)) 
    print("Unique Tweets: " + str(len(tweet_ids))) 
    self.save_parsed_file(all_tweets)

  def save_parsed_file(self,tweets):
    savefile = './parsed/parsed_tweets.json'
    with open(savefile,'w') as w_file:
      w_file.write('{}\n'.format(json.dumps(tweets)))
    print("Tweetcount: " + str(len(tweets)))
    print("File saved: " + savefile)

  def get_files_from_folder(self,folder):
    return [ folder + '/' + f for f in listdir(folder) if isfile(join(folder,f)) ]



tp = TweetParser()
tp.delete_duplicates(tp.get_files_from_folder('./data'))
    
