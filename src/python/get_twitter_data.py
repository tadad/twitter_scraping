import sys
import tweepy
import json
import psycopg2
import authentication # local environment config stuff
from datetime import datetime, timedelta

def load_angels(API, angels):
    """
    Takes in a Tweepy API and a list of angels and inserts it into the database
    @param API: Tweepy API instance
    @param angels: list of angels, organized as [{"handle":"name"}, ...]
    @returns: none
    """
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


def load_tweets(API, CONNECTION, days=7):
    """
    Gets all liked tweets from the angels table in the database.
    @param API: tweepy API instance
    @param CONNECTION: a connection to the postgres database using psycopg2
    @param days: number of days offset to get the likes from
    @returns: nothing
    """
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

def get_founders(CONNECTION):
    """
    @param CONNECTION: A connection to the postgres database using psycopg2
    @returns a list of accounts that the angels have liked in the past 7 days
    """
    cursor = CONNECTION.cursor()
    cursor.execute(open('src/sql/get_names.sql', 'r').read())
    data = cursor.fetchall()

    cursor.close()
    return data
  

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
        with open('../data/angels.json') as f:
            angels = json.load(f)
            load_angels(api, connection, angels)

    if '-t' in args or len(args)==0:
        load_tweets(api, connection)

    if '-g' in args or len(args)==0:
        founders = get_founders(connection)
        today = datetime.today().strftime('%Y-%m-%d')
        
        with open('src/data/{0}.json'.format(today), 'w+') as out:
            all_data = {'data': []}
            for row in founders:
                data = {
                    'angel_name':row[0],
                    'angel_handle':row[1],
                    'name': row[2],
                    'handle': row[3],
                    'bio': row[4], 
                    'date_liked': str(row[5])
                }
                all_data['data'].append(data)

            json.dump(all_data, out)    

    connection.close()
