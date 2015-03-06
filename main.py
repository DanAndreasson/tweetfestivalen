#!/usr/bin/python3

import re
import json
import pprint
import math
from collections import OrderedDict

STOP_WORDS = "vara vad kan sina här ha mot vid kunde något från ut när efter upp vi där min skulle då sin nu har mig du så till är men ett om hade på den med var sig en och det att var att jag i och eller som man melodifestivalen mello melfest".split()
BAD_CHARS = r"[,.?!-/;:']|(@.+ )"

artists = [
        'Andreas Weise – ”Bring Out the Fire”',
        'Linus Svenning – ”Forever Starts Today”',
        'Hasse Andersson – ”Guld och gröna skogar”',
        'Kristin Amparo – ”I See You”',
        'Dolly Style – ”Hello Hi”',
        'Dinah Nah – ”Make Me (La La La)”',
        'Behrang Miri feat. Victor Crone – ”Det rår vi inte för”',
        'Samir & Viktor - ”Groupie”',
        ]
UNKNOWN_WORDS = []
WORDS = []

chance_of_winning = {}

class NaiveBayesClassifier():
    pp = {}
    pc = {}
    pw = {}
    nr_of_tweets = 0

    def save(self, filename):
        with open(filename, 'w') as outfile:
            json.dump({"pw": self.pw, "pc": self.pc, "pp": self.pp}, outfile)

    def load(self, filename):
        with open(filename) as fp:
            data = json.load(fp)
            self.pw = data["pw"]
            self.pc = data["pc"]
            self.pp = data["pp"]

    def get_tokens(self, tweet):
        """Returns the token list for the specified tweet."""
        message = re.compile(BAD_CHARS, re.IGNORECASE).sub("", tweet["message"].lower())
        return [x for x in message.split() if x not in STOP_WORDS]

    def placements(self):
        return chance_of_winning

    def ensure_key(self, d, k, v):
        """If the key is not present, create it with v as value """
        if k not in d.keys():
            d[k] = v

    def predict_positive(self, tweet):

        tokens = self.get_tokens(tweet)
        positive = self.pc["positive"]
        negative = self.pc["negative"]
        
        for word in tokens:
            if word in self.pp["positive"]:
                positive += self.pp["positive"][word]

            if word in self.pp["negative"]:
                negative += self.pp["negative"][word]

        return positive > negative
    
        
    def predict(self, tweet):
        """Predicts the artist of the specified tweet."""
        self.nr_of_tweets += 1
        probable_artists = {}
        for k in self.pw:
            #probable_artists[k] = 0
            probable_artists[k] = self.pc[k]

        for token in self.get_tokens(tweet):
            WORDS.append(token)
            word_existed = False
            for artist in probable_artists:
                if token in self.pw[artist].keys():
                    word_existed = True
                    if probable_artists[artist] == 0:
                        probable_artists[artist] = (self.pw[artist][token])
                    else:
                        probable_artists[artist] += (self.pw[artist][token])
            if not word_existed:
                UNKNOWN_WORDS.append(token)



        winner = None
        for probable_artist, p in probable_artists.items():
            if winner == None:
                winner = probable_artist
            elif p > probable_artists[winner]:
                winner = probable_artist
        
        chance_of_winning[winner] += 1
        return winner
        


    def train_opinion(self, tweets):
        """Trains the parser on positive and negative tweets using specified training data"""
        smoothing_set = set()
        positive_words = negative_words = {}
        word_count = {}

        self.ensure_key(self.pc,"negative",0)
        self.ensure_key(self.pc,"positive",0)
        
        for tweet in tweets:
            tokens = self.get_tokens(tweet)
            if tweet["positive"]:
                self.pc["positive"] += 1
                for w in tokens:
                    smoothing_set.add(w)
                    self.ensure_key(positive_words,w,0)
                    self.ensure_key(word_count,w,0)
                    positive_words[w] += 1
                    word_count[w] += 1
            else:
                self.pc["negative"] += 1
                for w in tokens:
                    smoothing_set.add(w)
                    self.ensure_key(negative_words,w,0)
                    self.ensure_key(word_count,w,0)
                    negative_words[w] += 1
                    word_count[w] += 1
        
        self.pc["positive"] = math.log( self.pc["positive"] / len(tweets) )
        self.pc["negative"] = math.log( self.pc["negative"] / len(tweets) )
        self.pp["positive"] = positive_words
        self.pp["negative"] = negative_words


        for word in smoothing_set:
            for key in self.pp:
                self.ensure_key(self.pp[key],word,0)
                self.pp[key][word] += 1

        #TODO: word_count[w] and positive_words[w] or negative_words[w]
        #      calculates same things??? or too little data?
        for key, words in self.pp.items():
            for word, c in words.items():
                self.pp[key][word] = math.log( c / word_count[word] )
                
        
    def train(self, tweets):
        """Trains using the specified training data."""
        word_count = {}
        smoothing_set = set()
        positive_tweets = negative_tweets = 0
        for tweet in tweets:
            tokens = self.get_tokens(tweet)
            artist = artists[int(tweet["artist"])-1]
            # if tweet["positive"]:
            #     artist = artists[int(tweet["artist"])-1]
            # else:
            #     artist = "negative"
            #     negative_tweets += 1
            self.ensure_key(self.pc, artist, 0)
            self.pc[artist] += 1
            self.ensure_key(self.pw, artist, {})
            for w in tokens:
                smoothing_set.add(w)
                self.ensure_key(self.pw[artist], w, 0)
                self.pw[artist][w] += 1
                self.ensure_key(word_count, w, 0)
                word_count[w] += 1
        # print(str(negative_tweets) + " negativa tweets")
        print("Tränade på " + str(len(tweets)))

        
        for artist in self.pw:
            self.pc[artist] = math.log(self.pc[artist] / len(tweets))

        #add one smoothing
        for word in smoothing_set:
            for key in self.pw:
                self.ensure_key(self.pw[key],word,0)
                self.pw[key][word] += 1
        
        
        for artist, words in self.pw.items():
            for word, c in words.items():
                self.pw[artist][word] = math.log(c / word_count[word])



if __name__ == "__main__":
    import json
    import sys
    import os


    def LOG(msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

    if sys.argv[1] == "train":
        classifier = NaiveBayesClassifier()
        training_data = []
        for fn in os.listdir("./gold"):
            with open("./gold/" + fn) as fp:
                training_data += json.load(fp)
        LOG("Training ...")
        #remove comment to train opinion
        #classifier.train_opinion(training_data)
        classifier.train(training_data)
        LOG(" done\n")
        LOG("Saving model to %s ..." % sys.argv[3])
        classifier.save(sys.argv[3])
        LOG(" done\n")

    # Load a trained model from a file and evaluate it on test data.
    # Usage: python lab1.py evaluate MODEL_FILE TEST_DATA_FILE
    if sys.argv[1] == "evaluate":
        classifier = NaiveBayesClassifier()
        LOG("Loading the model from %s ..." % sys.argv[2])
        classifier.load(sys.argv[2])
        LOG(" done\n")
        with open(sys.argv[3]) as fp:
            LOG("Loading test data from %s ..." % sys.argv[3])
            test_data = json.load(fp)
            LOG(" done\n")
        for k in classifier.pw:
            chance_of_winning[k] = 0
        for tweet in test_data:
            #remove comment to remove negative tweets
            #if classifier.predict_positive(tweet):
            classifier.predict(tweet)
                
        for artist, points in classifier.placements().items():
            print( "{0:.1f}% {1}".format(abs(points/classifier.nr_of_tweets)*100, artist))
        print("\n" +str(classifier.nr_of_tweets) + " tweets was predicted")
        print(str(len(set(UNKNOWN_WORDS))) + " ord skippades")
        print(str(len(set(WORDS))) + " ord totalt")
        print(str((len(set(UNKNOWN_WORDS))/len(set(WORDS)))*100) + "% skippades" )
        #pprint.pprint(classifier.pw)
        #for word in set(UNKNOWN_WORDS):
        #    print(word, end=" ")
