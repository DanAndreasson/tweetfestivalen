#!/usr/bin/python3

import re
import json
import pprint
import math
from collections import OrderedDict

STOP_WORDS = "vara vad kan sina här ha mot vid kunde något från ut när efter upp vi där min skulle då sin nu har mig du så till är men ett om hade på den med var sig en och det att var att jag i och eller som man melodifestivalen mello melfest".split()
BAD_CHARS = r"[,.?!-/;:']"

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

chance_of_winning = {}

class NaiveBayesClassifier():
    pc = {}
    pw = {}
    nr_of_tweets = 0

    def save(self, filename):
        with open(filename, 'w') as outfile:
            json.dump({"pw": self.pw, "pc": self.pc}, outfile)

    def load(self, filename):
        with open(filename) as fp:
            data = json.load(fp)
            self.pw = data["pw"]
            self.pc = data["pc"]

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

    def predict(self, tweet):
        """Predicts the artist of the specified tweet."""
        self.nr_of_tweets += 1
        probable_artists = {}
        for k in self.pw:
            probable_artists[k] = 0
            chance_of_winning[k] = 0

        for token in self.get_tokens(tweet):
            for artist in probable_artists:
                if token in self.pw[artist].keys():
                    probable_artists[artist] += math.log2(self.pw[artist][token])
                else:
                    UNKNOWN_WORDS.append(token)

        winner = None
        for probable_artist, p in probable_artists.items():
            if winner == None:
                winner = probable_artist
            elif p > probable_artists[winner]:
                winner = probable_artist
        chance_of_winning[winner] += probable_artists[winner]



    def train(self, tweets):
        """Trains using the specified training data."""
        word_count = {}
        for tweet in tweets:
            tokens = self.get_tokens(tweet)
            artist = tweet["artist"]
            self.ensure_key(self.pc, artist, 0)
            self.pc[artist] += 1
            self.ensure_key(self.pw, artist, {})
            for w in tokens:
                self.ensure_key(self.pw[artist], w, 0)
                self.pw[artist][w] += 1
                self.ensure_key(word_count, w, 0)
                word_count[w] += 1

        for artist, words in self.pw.items():
            for word, c in words.items():
                self.pw[artist][word] = c / word_count[word]



if __name__ == "__main__":
    import json
    import sys

#    with open(sys.argv[1]) as fp:
#
#
#        print("Laddar tweets från %s ..." % sys.argv[1])
#        data = json.load(fp)
#    classifier = NaiveBayesClassifier()
#    classifier.train(data)
#    test_data = {"message": "raimond plockar detta lätt GRYM SOM FAN"}
#    classifier.predict(test_data)
#

    def LOG(msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

    if sys.argv[1] == "train":
        classifier = NaiveBayesClassifier()
        with open(sys.argv[2]) as fp:
            LOG("Loading training data from %s ..." % sys.argv[2])
            training_data = json.load(fp)
            LOG(" done\n")
        LOG("Training ...")
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
        for tweet in test_data:
            classifier.predict(tweet)
        for artist, points in classifier.placements().items():
            print( "{0:.3f} {1}".format(abs(points), artists[int(artist)-1]))
        print("\n" +str(classifier.nr_of_tweets) + " tweets was predicted")
        print(str(len(set(UNKNOWN_WORDS))) + " ord skippades")
        #for word in set(UNKNOWN_WORDS):
        #    print(word, end=" ")
