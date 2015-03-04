#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

class TweetArtistTagger:

  def __init__(self):
  	self.artist_tags = {
  		0: ["#*--None--*#"],
  		1: ["Andreas Weise"," Andreas ", " Weise", "Bring Out the Fire"],
  		2: ["Linus Svenning", " Linus ", " Svenning", "Forever Starts Today"],
  		3: ["Hasse Andersson", " Hasse", " kvinnaböske" " Andersson", "Guld och gröna skogar"],
  		4: ["Kristin Amparo", " Kristin", " Amparo", "I See You"],
  		5: ["Dolly Style", " Dolly", " Style", "Hello Hi"],
  		6: ["Dinah Nah", " Dinah", " Nah", "Make Me (La La La)", "La la la", "lalala", "lalala"],
  		7: ["Behrang Miri feat. Victor Crone", " Behrang", " Miri", " Victor", " Crone", "Det rår vi inte för"],
  		8: ["Samir & Viktor", " Samir", " Viktor", " Groupie", "#groupie"],
  	}

  def save_file(self,tweets):
    savefile = './parsed/relevant_tweets_with_predicted_artists.json'
    with open(savefile,'w') as w_file:
      w_file.write('{}\n'.format(json.dumps(tweets)))
    print("Tweetcount: " + str(len(tweets)))
    print("File saved: " + savefile)

     

  def load_from_file(self,filename):
    with open(filename, 'r') as read_file:
      return json.load(read_file)


  def tag(self, tweet):
  	foundArtists = []
  	for artist, tags in self.artist_tags.items():
  		lowercaseTweet = tweet["message"].lower()
  		for tag in tags:
  			if tag.lower() in lowercaseTweet:
  				foundArtists.append(artist)
  				break

  	if len(foundArtists) == 1:
  		tweet["artist"] = foundArtists[0]
  	else:
  		tweet["artist"] = 0

  	return tweet

  def start(self, tweet_file_path):
  	tweets = self.load_from_file(tweet_file_path)
  	taggedTweets = []
  	for tweet in tweets:
  		taggedTweets.append(self.tag(tweet))

  	for tagged in taggedTweets:
  		print("")
  		print(tagged["message"])
  		#print("TAGGED AS " + str(tweet["artist"]))
  		print("TAGGED AS " + self.artist_tags[tagged["artist"]][0])
  	
  	self.save_file(taggedTweets)

artistTagger = TweetArtistTagger()

artistTagger.start('./parsed/relevant_tweets.json')