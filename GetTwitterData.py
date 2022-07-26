
# https://datascienceparichay.com/article/get-data-from-twitter-api-in-python-step-by-step-guide/

import tweepy as tw
import pandas as pd
import os
from dotenv import load_dotenv

def GetTwitterData():
    # to make columns wider. Use if need print out a single column
    pd.set_option('max_colwidth', -1)

    # your twitter API key and API secret
    load_dotenv()
    my_api_key = os.getenv("api_key")
    my_api_secret = os.getenv("api_secret")


    # authenticate
    auth = tw.OAuthHandler(my_api_key, my_api_secret)
    api = tw.API(auth, wait_on_rate_limit=True)


    # what tweets are you looking for?
    search_query = "#putin -filter:retweets"


    # get tweets from the API
    tweets = tw.Cursor(api.search_tweets,
                q=search_query,
                lang="en",
                since="2022-07-01").items(3)
    # store the API responses in a list
    tweets_copy = []
    # The responses are iterated over and saved to the list tweets_copy.
    for tweet in tweets:
        tweets_copy.append(tweet)
        
    print("Total Tweets fetched:", len(tweets_copy))

    ########## create a dataset (a pandas dataframe) using the attributes of the tweets received from the API. ###############

    # initialize the dataframe
    tweets_df = pd.DataFrame()

    # populate the dataframe
    for tweet in tweets_copy:
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            # calling the API again with the tweet id and fetching its full text. 
            # This is because tweet.text does not contain the full text of the Tweet.
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
            
        except:
            pass
        tweets_df = tweets_df.append(pd.DataFrame({ 'user_name': tweet.user.name,
                                                    'user_location':tweet.user.location,#\
                                                    'user_description':tweet.user.description,
                                                    'user_verified': tweet.user.verified,
                                                    'date': tweet.created_at,
                                                    'text': text,
                                                    'hashtags': [hashtags if hashtags else None],
                                                    'source': tweet.source}))

        tweets_df=tweets_df.reset_index(drop=True)
        

    # show the dataframe
    # print(tweets_df.head())

    # print all rows and only column "text"
    print(tweets_df.iloc[:,[5]])
    return

def main():
    tw_data = GetTwitterData()


if __name__ == "__main__":
    main()