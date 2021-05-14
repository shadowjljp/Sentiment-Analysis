from kafka import KafkaProducer
import re
import kafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# TWITTER API CONFIGURATIONS
consumer_key = "US2mlNT4wu39dlBivxG2MGarw"
consumer_secret = "L0qBsYhbL6eP8oD4vuL6jSAIpJnprtnDOkrWDM43EyhnuLQRmf"
access_token = "924968073727115264-0WDxFOBl8Ix4aq3wRWzOLe4dWuCIyCT"
access_secret = "LZ86wj0O8gjp8gZTBcF8T0Q5wBAkNvVyj7bamOKBQ9R9u"

# TWITTER API AUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# Twitter Stream Listener
class Scrappy(StreamListener):
    def __init__(self):
        # localhost:9092 = Default Zookeeper Producer Host and Port Addresses
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    # Get Producer that has topic name is Twitter
    # self.producer = self.client.topics[bytes("twitter")].get_producer()

    def on_data(self, data):
        # Producer produces data for consumer
        # Data comes from Twitter

        #remove invlid symbols
        data = re.sub(r'[^\x00-\x7F]+', " ", data)
        data = re.sub('RT @\\w+:', " ", data)
        #data = re.sub(r'http\S+', "", data)
        #data = re.sub(r'\n+', " ", data)
        self.producer.send("twitter", data.encode('utf-8'))
        print(data)
        return True

    def on_error(self, status):
        if status == 420:
            # returning False in on_error disconnects the stream
            return False
        print(status)
        return True


# Twitter Stream Config
twitter_stream = Stream(auth, Scrappy())

# Produce Data that has trump hashtag (Tweets)
twitter_stream.filter(track=['#vaccine', '#coronavirus', '#trump'])