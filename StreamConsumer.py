from kafka import KafkaConsumer
import json
# from elasticsearch import Elasticsearch
from textblob import TextBlob
from elasticsearch import Elasticsearch
import nltk
from SentimentAnalyzerNLTK import SentimentAnalyze

nltk.downloader.download('vader_lexicon')
es = Elasticsearch()


# tweet_list = []
# neutral_list = []
# negative_list = []
# positive_list = []


def main():
    '''
    main function initiates a kafka consumer, initialize the tweetdata database.
    Consumer consumes tweets from producer, extracts features, cleanses the tweet text,
    calculates sentiments and loads the data into elasticsearch
    '''
    # set-up a Kafka consumer
    consumer = KafkaConsumer("twitter")
    for msg in consumer:
        dict_data = json.loads(msg.value)
        tweet = TextBlob(dict_data["text"])
        print(tweet)

        # from NLTK sentiment analyze

        sentiment = ""
        sentiment = SentimentAnalyze(sentiment, tweet)
        print('sentiment is ',sentiment)
        # add text and sentiment info to elasticsearch
        es.index(index="sitrep",
                 doc_type="test-type",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": dict_data["created_at"],
                       "message": dict_data["text"],
                       "sentiment":sentiment,
                       "polarity":tweet.sentiment.polarity
                       })
        print('\n')



if __name__ == "__main__":
    main()
