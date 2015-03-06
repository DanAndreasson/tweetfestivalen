#!/usr/bin/python3

import re
import json
import pprint
import math
from collections import OrderedDict
import operator

STOP_WORDS = "vara vad kan sina här ha mot vid kunde något från ut när efter upp vi där min skulle då sin nu har mig du så till är men ett om hade på den med var sig en och det att var att jag i och eller som man melodifestivalen mello melfest".split()
BAD_CHARS = r"[,.?!-/;:']|(@.+ )"


artist_regexes = {
    #'Andreas Weise – ”Bring Out the Fire”',
    1: r"( arne)|(w(e|a)(i|j)se)|(bring out the fi+re)",

    #'Linus Svenning – ”Forever Starts Today”',
    2: r"(linus)|(sven+ing)|(forever starts today)",

    #'Hasse Andersson – ”Guld och gröna skogar”',
    3: r"(has+e)|(anders+on)|(g(u|o)ld (och|\&) gr(ö|o)na skogar)",

    #'Kristin Amparo – ”I See You”',
    4: r"((k|c)ristin)|(amparo)|(i se+ (you|u))",

    #'Dolly Style – ”Hello Hi”',
    5: r"(dol+y)|(hel+o hi)",

    #'Dinah Nah – ”Make Me (La La La)”',
    6: r"(dinah)|(nah)|(make me)|(la la)|(lala)",

    #'Behrang Miri feat. Victor Crone – ”Det rår vi inte för”',
    7: r"(behrang)|(miri)|(cro+ne)|(det? rår vi inte för)",

    #'Samir & Viktor - ”Groupie”',
    8: r"(sami+r)|(badra+n)|( samme )|(viktor)|((\#)?groupie?)",
}


artists = [
        'No Artist Found',
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

    def accuracy(self, tweets):
        """Computes accuracy on the specified test data."""
        num_documents = 0
        num_correct = 0
        for tweet in tweets:
            num_documents += 1
            if int(tweet["artist"]) == self.predict(tweet)["artist"] and tweet["positive"] == self.predict_positive(tweet):
                num_correct += 1

        return num_correct/num_documents

    def accuracy_artist(self, tweets):
        """Computes accuracy on the specified test data."""
        num_documents = 0
        num_correct = 0
        for tweet in tweets:
            num_documents += 1
            if int(tweet["artist"]) == self.predict(tweet)["artist"]:
                num_correct += 1
        return num_correct/num_documents

    def accuracy_opinion(self, tweets):
        """Computes accuracy on the specified test data."""
        num_documents = 0
        num_correct = 0
        for tweet in tweets:
            num_documents += 1
            if tweet["positive"] == self.predict_positive(tweet):
                num_correct += 1
        return num_correct/num_documents

    def precision_artist(self, c, tweets):
        """Computes precision for class `c` on the specified test data."""
        truepositives = 0
        falsepositives = 0
        for tweet in tweets:
            predicted = self.predict(tweet)["artist"]
            if (int(tweet["artist"]) == c) and (predicted == c):
                truepositives += 1
            elif (int(tweet["artist"]) != c) and (predicted == c):
                falsepositives += 1

        return truepositives/(truepositives + falsepositives)


    def precision_opinion(self, c, tweets):
        """Computes precision for class `c` on the specified test data."""
        truepositives = 0
        falsepositives = 0
        for tweet in tweets:
            predicted = self.predict_positive(tweet)
            if (tweet["positive"] == c) and (predicted == c):
                truepositives += 1
            elif (tweet["positive"] != c) and (predicted == c):
                falsepositives += 1
        if truepositives + falsepositives == 0:
            return "No truepositives or falsepositives"
        return truepositives/(truepositives + falsepositives)

    def recall_artist(self, c, tweets):
        """Computes recall for class `c` on the specified test data."""
        truepositives = 0
        falsenegatives = 0
        for tweet in tweets:
            predicted = self.predict(tweet)["artist"]
            if (int(tweet["artist"]) == c) and (predicted == c):
                truepositives += 1
            elif (int(tweet["artist"]) == c) and (predicted != c):
                falsenegatives += 1
        return truepositives/(truepositives + falsenegatives)
                
    def recall_opinion(self, c, tweets):
        """Computes recall for class `c` on the specified test data."""
        truepositives = 0
        falsenegatives = 0
        for tweet in tweets:
            predicted = self.predict_positive(tweet)
            if (tweet["positive"] == c) & (predicted == c):
                truepositives += 1
            elif (tweet["positive"] == c) & (predicted != c):
                falsenegatives += 1
        return truepositives/(truepositives + falsenegatives)

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

        return positive >= negative
    
        
    def predict(self, tweet):
        """Predicts the artist of the specified tweet."""
        foundArtists = []
        lowercaseTweet = tweet["message"].lower()
        for artist, regex in artist_regexes.items():
            reg = re.compile(regex, re.IGNORECASE)
            r = reg.search(lowercaseTweet)
            if r:
                foundArtists.append(artist)

        if len(foundArtists) == 1:
            tweet["artist"] = foundArtists[0]
        else:
            tweet["artist"] = 0

        return tweet        

    def train_opinion(self, tweets):
        """Trains the parser on positive and negative tweets using specified training data"""
        smoothing_set = set()
        numspeechesleft = 0
        numspeechesright = 0
        totaltokensleft = 0
        totaltokensright = 0

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

        for key, words in self.pp.items():
            for word, c in words.items():
                if key == "positive":
                    self.pp[key][word] = math.log( c / positive_count + len(smoothing_set))
                else:
                    self.pp[key][word] = math.log( c / negative_count + len(smoothing_set))
                
    #Tested and working
    def train_opinion_new(self, tweets):
        """Trains using the specified training data."""
        numspeechespositive = 0#left
        numspeechesnegative = 0
        totaltokenspositive = 0#left
        totaltokensnegative = 0
        self.pp["positive"] = {}
        self.pp["negative"] = {}

        #Build vocabulary and gather frequencies
        for tweet in tweets:
            if tweet["positive"]:
                numspeechespositive += 1
                for token in self.get_tokens(tweet):
                    totaltokenspositive += 1
                    if token in self.pp["positive"]:
                        self.pp["positive"][token] += 1
                    else:
                        self.pp["positive"][token] = 1
                    if token not in self.pp["negative"]: #Make sure this token exists in both R and L dictionaries
                        self.pp["negative"][token] = 0

            else:
                numspeechesnegative += 1
                for token in self.get_tokens(tweet):
                    totaltokensnegative += 1
                    if token in self.pp["negative"]:
                        self.pp["negative"][token] += 1
                    else:
                        self.pp["negative"][token] = 1
                    if token not in self.pp["positive"]: #Make sure this token exists in both R and L dictionaries
                        self.pp["positive"][token] = 0
    
        #Calculate relative frequencies. Add-one smoothing. len(self.pw["L/R"]) is the number of unique words in the training data, i.e. the vocabulary length.
        for token in self.pp["positive"]:
            self.pp["positive"][token] = math.log((self.pp["positive"][token]+1.0)/(totaltokenspositive+len(self.pp["positive"]))) 
        for token in self.pp["negative"]:
            self.pp["negative"][token] = math.log((self.pp["negative"][token]+1.0)/(totaltokensnegative+len(self.pp["negative"])))

        #Calculate class frequencies
        self.pc["positive"] = math.log(numspeechespositive/(numspeechespositive + numspeechesnegative))
        self.pc["negative"] = math.log(numspeechesnegative/(numspeechespositive + numspeechesnegative))

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
        classifier.train_opinion_new(training_data)
        #classifier.train(training_data)
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

        numtrue = 0
        numfalse = 0
        artist_pos_count = {}
        predicted_tweets =[]

        for tweet in test_data:
            predicted_tweets.append(classifier.predict(tweet))
            #print(tweet)
            #remove comment to remove negative tweets
            if classifier.predict_positive(tweet):
                predicted_artist = artists[classifier.predict(tweet)["artist"]]
                classifier.ensure_key(artist_pos_count, predicted_artist, 0)
                artist_pos_count[predicted_artist] += 1
                numtrue += 1
                if predicted_artist == artists[8]:
                    print(tweet["message"])
                    print()
            else:
                numfalse += 1
        
        print(numtrue)
        print(numfalse)
        print(sorted(artist_pos_count.items(),key=operator.itemgetter(1)))
        #for artist, points in classifier.placements().items():
        #    print( "{0:.1f}% {1}".format(abs(points/classifier.nr_of_tweets)*100, artist))
        #print("\n" +str(classifier.nr_of_tweets) + " tweets was predicted")
        #print(str(len(set(UNKNOWN_WORDS))) + " ord skippades")
        #print(str(len(set(WORDS))) + " ord totalt")
        #print(str((len(set(UNKNOWN_WORDS))/len(set(WORDS)))*100) + "% skippades" )

        #Utskrifter för accuracy, precision & recall:
        
        #print("Accuracy: " + str(classifier.accuracy(test_data)))
        #print("Accuracy för artister: " + str(classifier.accuracy_artist(test_data)))
        #print("Accuracy för åsikt: " + str(classifier.accuracy_opinion(test_data)))
        #for x in range(0,8):
        #    print(str(artists[x]) + " - Precision: " + str(classifier.precision_artist(x,test_data)) 
        #        + ", Recall: " + str(classifier.recall_artist(x,test_data)))
        #print("Precision för positiva taggar: " + str(classifier.precision_opinion(True,test_data)))
        #print("Precision för negativa taggar: " + str(classifier.precision_opinion(False,test_data)))
        #print("Recall för positiva taggar: " + str(classifier.recall_opinion(True,test_data)))
        #print("Recall för negativa taggar: " + str(classifier.recall_opinion(False,test_data)))
        #pprint.pprint(classifier.pw)
        #for word in set(UNKNOWN_WORDS):
        #    print(word, end=" ")
