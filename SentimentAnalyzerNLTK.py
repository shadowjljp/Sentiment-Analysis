from nltk.sentiment.vader import SentimentIntensityAnalyzer


def SentimentAnalyze(sentiment, tweet):
    pos = 0
    neg = 0
    neu = 0
    score = SentimentIntensityAnalyzer().polarity_scores(str(tweet))
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    if neg > pos:
        sentiment = "negative"
    elif pos > neg:
        sentiment = "positive"
    elif pos == neg:
        sentiment = "neutral"
    return sentiment


# LOCAL DATAFRAME USE ONLY score and catorgorize tweets
def SentimentAnalyzeLOCAL(tweet):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    global polarity
    polarity += tweet.sentiment.polarity

    if neg > pos:
        negative_list.append(tweet)
        global negative
        negative += 1
    elif pos > neg:
        positive_list.append(tweet)
        global positive
        positive += 1
    elif pos == neg:
        neutral_list.append(tweet)
        global neutral
        neutral += 1
