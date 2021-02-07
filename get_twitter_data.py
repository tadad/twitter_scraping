import sys
import tweepy
import json
import psycopg2
import authentication
from datetime import datetime, timedelta

def load_angels(API, CONNECTION, angels):
    connection = psycopg2.connect(
                                  user="drew",
                                  password=authentication.DB_PW,
                                  host="127.0.0.1",
                                  port="5432",
                                  database="twitter")
    
    cursor = connection.cursor()
    insert_query = "INSERT INTO angels(id, handle, name) VALUES('{0}', '{1}', '{2}') ON CONFLICT DO NOTHING"

    for angel in angels:
        user = API.get_user(angel)
        # get bio with user.description
        query = insert_query.format(user.id, user.screen_name, user.name)            
        cursor.execute(query)
        connection.commit()
    
    cursor.close()


def get_tweets(API, CONNECTION, days=7):
    DATE_CUTOFF = datetime.now() - timedelta(days=days)
    
    cursor = connection.cursor()

    select_query = "SELECT id, handle FROM angels"
    cursor.execute(select_query)
    angels = cursor.fetchall()
    
    for angel in angels:
        for favorite in tweepy.Cursor(API.favorites, id=angel[1]).items(100):
            # not ideal but can't do better. API doesn't give like timestamp
            if DATE_CUTOFF > favorite.created_at:
                break
            
            tweet_insert = "INSERT INTO tweets(id, tweet, created_at, author_id, liked_by_id) VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
            founder_insert = "INSERT INTO potential_founders(id, handle, name, description) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING"
            
            cursor.execute(founder_insert, (favorite.user.id,
                                     favorite.user.screen_name,
                                     favorite.user.name,
                                     favorite.user.description))

            CONNECTION.commit()

            cursor.execute(tweet_insert, (favorite.id,
                                   favorite.text,
                                   favorite.created_at,
                                   favorite.user.id,
                                   angel[0]))
            
            CONNECTION.commit()
    cursor.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    
    auth = tweepy.OAuthHandler(authentication.API_KEY, authentication.API_SECRET_KEY)
    auth.set_access_token(authentication.ACCESS_TOKEN, authentication.ACCESS_SECRET)
    api = tweepy.API(auth)

    connection = psycopg2.connect(
                                  user="drew",
                                  password=authentication.DB_PW,
                                  host="127.0.0.1",
                                  port="5432",
                                  database="twitter")

    if '-a' in args or len(args)==0: 
        with open('./angels.json') as f:
            angels = json.load(f)
            load_angels(api, connection, angels)
    
    if '-t' in args or len(args)==0:
        get_tweets(api, connection)

    connection.close()
