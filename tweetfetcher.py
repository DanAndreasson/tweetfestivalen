from TwitterSearch import *
import time
import json
import datetime
import os.path

class TweetFetcher:
    
    def __init__(self):
        self.keywords = ['melfest','mello2015','melodifestivalen','mello15','mello','melodifestivalen2015','melodifestivalen15']
        self.twitter = TwitterSearch(
                consumer_key='7C2iVk5rnJEmlLd11eGqKOzkN',
                consumer_secret='ZUXVMhEvuT1jlviDyimApDT9MxHWw6hbYhRSJWDNmFkdWPTAxh',
                access_token='133211494-rpP813evJKZVVmS7M3nAK5BSAGpa31O21kgml5i7',
                access_token_secret='aHk3sp5B6hHj8xYqEfHmkzfglHN3uWwrAb9JkbrcKAdjl')
        self.tweet_list = []

    def search(self):
        try:
            for key in self.keywords:
                tso = TwitterSearchOrder()
                tso.set_keywords([key])
                tso.set_include_entities(True)
                tso.set_language('sv')
                total_get = 0
                rate_counter = 0
                sleep_at = 1000
                sleep_for = 60
                print("Starting Search... - " + str(key))
                for tweet in self.twitter.search_tweets_iterable(tso):
                    hashtags = []
                    for tag in tweet['entities']['hashtags']:
                        hashtags.append(tag['text'])

                    json_d = {
                        "message" : tweet['text'],
                        "date": tweet['created_at'], 
                        "hashtags": hashtags,
                        "user": tweet['user']['screen_name'],
                        "retweet_count": tweet['retweet_count'],
                        "id": tweet['id'],
                    }

                    self.tweet_list.append(json_d)
                    rate_counter += 1
                    total_get += 1
                    if rate_counter >= sleep_at:
                        print("Search Complete...Sleeping...")
                        print('Current count: ' + str(total_get))
                        rate_counter = 0
                        self.save(self.tweet_list,key)
                        self.tweet_list = []
                        time.sleep(sleep_for)
        except TwitterSearchException as e:
            print(e)


    def save(self,tweets,keyword):
        print("Saving file...")
        filepath = "./data/"+ keyword + '-' + str(datetime.datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')) + ".json"
        with open(filepath, "w") as json_file:
            json_file.write("{}\n".format(json.dumps(tweets)))
        print("File Saved! - " + filepath)
        

    
fetcher = TweetFetcher()
fetcher.search()
fetcher.save(fetcher.tweet_list,'closing')
