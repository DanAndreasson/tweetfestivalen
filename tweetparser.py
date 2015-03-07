from os import listdir
import json
import datetime
from pytz import timezone
import pytz
from os.path import isfile, join
utc = pytz.utc
class TweetParser:

  def __init__(self):
    self.trigger_words = ["Andreas","Weise","Bring out the fire","Linus","Svenning",
        "Forever starts today","Hasse Andersson","Guld och gröna skogar",
        "Kristin","Amparo",
        "I see you","Dolly","Style","Hello hi","Dinah Nah",
        "Make me","la la la","Behrang","Miri","Victor","Crone","Det rår vi inte för",
        "Samir",",Badran","Viktor","Groupie"]
  
  def delete_duplicates(self,files,folder):
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
    self.save_parsed_file(all_tweets,folder)

  def save_parsed_file(self,tweets,folder):
    savefile = './parsed/'+folder+'/parsed_tweets.json'
    with open(savefile,'w') as w_file:
      w_file.write('{}\n'.format(json.dumps(tweets)))
    print("Tweetcount: " + str(len(tweets)))
    print("File saved: " + savefile)

  def save_relevant_file(self,tweets,date):
    savefile = './parsed/relevant_tweets - '+ date.isoformat() +'.json'
    with open(savefile,'w') as w_file:
      w_file.write('{}\n'.format(json.dumps(tweets)))
    print("Tweetcount: " + str(len(tweets)))
    print("File saved: " + savefile)

  def get_date(self,datestr):
    return datetime.datetime.strptime(datestr,"%a %b %d %H:%M:%S %z %Y")

  def relevant_tweet(self,tweet):
    message = tweet["message"]
    if any(word.lower() in message.lower() for word in self.trigger_words):
        return True
    return False

  def find_relevant_tweets(self,filename,date=None):
    all_tweets = []
    found_tweets = 0

    if date is not None:
      date = utc.localize(date)

    with open(filename, 'r') as read_file:
      tweets = json.load(read_file)
      for tweet in tweets:
        if date is not None:
          if self.get_date(tweet["date"]) < date:
            continue
        if self.relevant_tweet(tweet):
            found_tweets += 1
            all_tweets.append(tweet)

    self.save_relevant_file(all_tweets,date)

  def get_files_from_folder(self,folder):
    return [ folder + '/' + f for f in listdir(folder) if isfile(join(folder,f)) ]

#tp = TweetParser()
#from_date = datetime.datetime(2015,3,1)
#tp.find_relevant_tweets('./parsed/parsed_tweets.json',date=from_date)

