import os
import json
from tweetartisttagger import TweetArtistTagger

class GoldStandardTagger:

  def __init__(self):
    self.artist_tagger = TweetArtistTagger()
    self.artists = [
        'None',
        'Andreas Weise – ”Bring Out the Fire”',
        'Linus Svenning – ”Forever Starts Today”',
        'Hasse Andersson – ”Guld och gröna skogar”',
        'Kristin Amparo – ”I See You”',
        'Dolly Style – ”Hello Hi”',
        'Dinah Nah – ”Make Me (La La La)”',
        'Behrang Miri feat. Victor Crone – ”Det rår vi inte för”',
        'Samir & Viktor - ”Groupie”',
        ]

  def start(self,filename):
    
    tweets = self.load_from_file(filename)
    save_gold_tweets = [] 
    for tweet in tweets:
      self.clear_screen()
      print("GoldCount: " + str(len(save_gold_tweets)))
      tweet = self.print_screen(tweet) 
      if tweet == "QUIT":
        break
      if tweet != None:
        save_gold_tweets.append(tweet)
    self.save_file(save_gold_tweets) 

  def save_file(self,tweets):
    savefile = './gold/gold_tweets.json'
    with open(savefile,'w') as w_file:
      w_file.write('{}\n'.format(json.dumps(tweets)))
    print("Tweetcount: " + str(len(tweets)))
    print("File saved: " + savefile)


  def print_screen(self,tweet):
    print("Save and quit with q")
    print("Artister: (ignore_with: 0)")
    i = 1
    for a in self.artists:
      print(str(i) + ": " + a)
      i += 1
    print('\n')
    print("@" + tweet['user'])
    print(tweet['message'])
    
    tweet = self.artist_tagger.tag(tweet)
    if int(tweet["artist"] == 0):
      return None
    print("Predicted Artist: " + str(self.artists[int(tweet["artist"])]))

    positive = input("Positive? (y(1)/n(2)/ignore(3)/change_artist(4):")
    
    if positive == "4":
      artist = input("Artist:")
      tweet["artist"] = artist
      print("Predicted Artist: " + str(self.artists[int(tweet["artist"])]))
      positive = input("Positive? (y(1)/n(2)/ignore(3)/change_artist(4):")
    if positive == "q":
      return "QUIT"
    if positive == "3":
      return None
    positive = True if positive == "1" else False
    tweet["positive"] = positive
    return tweet
    

  def clear_screen(self):
      os.system('clear')
     

  def load_from_file(self,filename):
    with open(filename, 'r') as read_file:
      return json.load(read_file)


gst = GoldStandardTagger()

gst.start('./parsed/relevant_tweets.json')
