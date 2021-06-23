from flask import Flask, render_template, request, redirect, url_for
from joblib import load
# from get_tweets import get_related_tweets
import tweepy
import time
import pandas as pd
pd.set_option('display.max_colwidth', 1000)

# api key
api_key = "1qRm35j3kskUyITp8FquUk3Sj"
# api secret key
api_secret_key = "bdzrMnivVpi5ku4i1Dd4Dpmxdyo1oWjsnQNUvHPAZWRaKuAroi"
# access token
access_token = "158240218-M7DsUlvQKmxOtjfnKxFNKBTEmheuvNn4vi0MM6BP"
# access token secret
access_token_secret = "oWY5G9sTxnH81tFbaicN5DKs1AjkD2WsWM5oCyoSh8NoR"

authentication = tweepy.OAuthHandler(api_key, api_secret_key)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True)

def get_related_tweets(text_query):
    # list to store tweets
    tweets_list = []
    # no of tweets
    count = 50
    try:
        # Pulling individual tweets from query
        for tweet in api.search(q=text_query, count=count):
            print(tweet.text)
            # Adding to list that contains all tweets
            tweets_list.append({'created_at': tweet.created_at,
                                'tweet_id': tweet.id,
                                'tweet_text': tweet.text})
        return pd.DataFrame.from_dict(tweets_list)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)


pipeline = load("text_classification.joblib")


def requestResults(name):
    tweets = get_related_tweets(name)
    tweets['prediction'] = pipeline.predict(tweets['tweet_text'])
    # data = str(tweets.prediction.value_counts()) + '\n\n'
    return tweets


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        user = request.form['search']
        return redirect(url_for('success', name=user))


@app.route('/success/<name>')
def success(name):
    res = requestResults(name)
    pred = res['prediction'].tolist()
    data = res['tweet_text'].tolist()
    tweet_id = res['tweet_id'].tolist()
    n = len(data)
    return render_template('result.html', pred=pred, data=data, key = name, n = n, tweet_id = tweet_id)

if __name__ == '__main__' :
    app.run(debug=True)