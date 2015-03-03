#!/usr/bin/python3

import re
import pprint
import math

STOP_WORDS = "sissådär var att jag".split()
BAD_CHARS = r"[,.?!]"

ARTISTS = "pepcha raimond".split()

pc = dict.fromkeys(ARTISTS, 0.0)
pw = dict.fromkeys(ARTISTS, {})

UNKNOWN_WORDS = []

class NaiveBayesClassifier():

    def get_tokens(self, tweet):
        """Returns the token list for the specified tweet."""
        message = re.compile(BAD_CHARS, re.IGNORECASE).sub("", tweet["message"].lower())
        return [x for x in message.split() if x not in STOP_WORDS]

    def is_positive(self, tweet):
        """Returns true if a tweet is positive."""
        pass

    def get_artist(self, tweet):
        """Returns the artist of the specified tweet."""
        pass

    def accuracy(self, tweets):
        """Computes accuracy on the specified test data."""
        pass

    def precision(self, c, tweets):
        """Computes precision for class `c` on the specified test data."""
        pass

    def recall(self, c, tweets):
        """Computes recall for class `c` on the specified test data."""
        pass

    def predict(self, tweet):
        """Predicts the artist of the specified tweet."""
        probable_artists = dict.fromkeys(ARTISTS, 0)
        for token in self.get_tokens(tweet):
            for artist in probable_artists:
                if token in pw[artist].keys():
                    print(token)
                    print(pw[artist][token])
                    print(math.log(pw[artist][token]))
                    probable_artists[artist] += math.log(pw[artist][token])
        pprint.pprint(probable_artists)


    def train(self, tweets):
        """Trains using the specified training data."""
        word_count = {}
        for tweet in tweets:
            tokens = self.get_tokens(tweet)
            artist = tweet["artist"]
            pc[artist] += 1
            for w in tokens:
                if w not in pw[artist].keys():
                    pw[artist][w] = 0
                pw[artist][w] += 1
                if w not in word_count.keys():
                    word_count[w] = 0
                word_count[w] += 1

        for artist, words in pw.items():
            for word, c in words.items():
                pw[artist][word] = c / word_count[word]



if __name__ == "__main__":
    import json
    import sys

    with open(sys.argv[1]) as fp:
        print("Laddar tweets från %s ..." % sys.argv[1])
        data = json.load(fp)
    classifier = NaiveBayesClassifier()
    classifier.train(data)
    test_data = {"message": "raimond plockar detta lätt GRYM SOM FAN"}
    classifier.predict(test_data)


    #def LOG(msg):
    #    sys.stdout.write(msg)
    #    sys.stdout.flush()

    # Train a model on training data and save it to a file.
    # Usage: python lab1.py train TRAINING_DATA_FILE MODEL_FILE
    #if sys.argv[1] == "train":
    #    classifier = NaiveBayesClassifier()
    #    with open(sys.argv[2]) as fp:
    #        LOG("Loading training data from %s ..." % sys.argv[2])
    #        training_data = json.load(fp)
    #        LOG(" done\n")
    #    LOG("Training ...")
    #    classifier.train(training_data)
    #    LOG(" done\n")
    #    LOG("Saving model to %s ..." % sys.argv[3])
    #    classifier.save(sys.argv[3])
    #    LOG(" done\n")

    ## Load a trained model from a file and evaluate it on test data.
    ## Usage: python lab1.py evaluate MODEL_FILE TEST_DATA_FILE
    #if sys.argv[1] == "evaluate":
    #    classifier = MyNaiveBayesClassifier()
    #    LOG("Loading the model from %s ..." % sys.argv[2])
    #    classifier.load(sys.argv[2])
    #    LOG(" done\n")
    #    with open(sys.argv[3]) as fp:
    #        LOG("Loading test data from %s ..." % sys.argv[3])
    #        test_data = json.load(fp)
    #        LOG(" done\n")
    #    LOG("accuracy = %.4f\n" % classifier.accuracy(test_data))
    #    for c in sorted(classifier.pc):
    #        p = classifier.precision(c, test_data)
    #        r = classifier.recall(c, test_data)
    #        LOG("class %s: precision = %.4f, recall = %.4f\n" % (c, p, r))
