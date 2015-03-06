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
            6: ["Dinah Nah", " Dinah", " Nah", "Make Me (La La La)", "La la la", "lalala"],
            7: ["Behrang Miri feat. Victor Crone", " Behrang", " Miri", " Victor", " Crone", "Det rår vi inte för"],
            8: ["Samir & Viktor", " Samir", " Viktor", " Groupie", "#groupie"],
        }
        self.andrachansen = {
            1: ["Andreas Weise",                    "Bring out the Fire", [], []],
            2: ["Linus Svenning",                   "Forever Starts Today", [], []],
            3: ["Hasse Andersson",                  "Guld och gröna skogar", ["kvinnaböske"], []],
            4: ["Kristin Amparo",                   "I See You", [], []],
            5: ["Dolly Style",                      "Hello Hi", [], []],
            6: ["Dina Nah",                         "Make Me (La La La)", [], ["la la la", "lalala"]],
            7: ["Behrang Miri feat. Victor Crone",  "Det rår vi inte för", [], []],
            8: ["Samir & Viktor",                   "Groupie", [], []],
        }
        
        #self.part1..

    def get_artist_keywords(self, whole_name, song_name, known_artist_aliases = [], known_song_aliases = []):
        result = []
        #Name
        result.append(whole_name)
        name_entities =  list(filter(lambda word: word != "feat" and word != "ft", filter(None, [''.join(e for e in word if e.isalnum()) for word in whole_name.split()])))
        name_entities = [" " + word + " " for word in name_entities]
        name_entity_conjugations = []
        for word in name_entities:
            if not word.endswith("s "):
                name_entity_conjugations.append(" " + word.replace(" ","") + "s ")

        result = result + name_entities + name_entity_conjugations
        song_hashtag = "#" + ''.join(e for e in song_name.lower() if e.isalnum())
        if song_hashtag not in known_song_aliases:
            result.append(song_hashtag)

        result = result + known_artist_aliases + known_song_aliases
        return result

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

    def set_artist_lineup(self, competition):
        self.artist_tags[0] = "#*--None--*#"
        if competition == "andrachansen":
            for key, value in self.andrachansen.items():
                self.artist_tags[key] = self.get_artist_keywords(value[0], value[1], value[2], value[3])



    def start(self, tweet_file_path):
        self.set_artist_lineup("andrachansen")
        print(self.artist_tags)
        tweets = self.load_from_file(tweet_file_path)
        taggedTweets = []
        for tweet in tweets:
            taggedTweets.append(self.tag(tweet))

        #for tagged in taggedTweets:
        #   print("")
        #   print(tagged["message"])
            #print("TAGGED AS " + str(tweet["artist"]))
        #   print("TAGGED AS " + self.artist_tags[tagged["artist"]][0])
        
        #self.save_file(taggedTweets)

#artistTagger = TweetArtistTagger()

#artistTagger.start('./parsed/relevant_tweets.json')