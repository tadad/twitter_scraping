import tweepy
import json
import psycopg2
import authentication
from datetime import datetime, timedelta

DATE_CUTOFF = datetime.now() - timedelta(days=7)

auth = tweepy.OAuthHandler(authentication.API_KEY, authentication.API_SECRET_KEY)
auth.set_access_token(authentication.ACCESS_TOKEN, authentication.ACCESS_SECRET)
api = tweepy.API(auth)

try:
    connection = psycopg2.connect(user="drew",
                                 password=authentication.DB_PW,
                                 host="127.0.0.1",
                                 port="5432",
                                 database="twitter"
                                )
    print(connection.get_dsn_parameters())

    cur = connection.cursor()
    cur.execute('SELECT version()')
    print(cur.fetchone())

    cur.close()






except:
    print('error')


with open('./angels.json') as f:
    angels = json.load(f)
    
# 
# for angel in angels:
#     for favorite in tweepy.Cursor(api.favorites, id=angel).items(100):
#         # not ideal but can't do better. API doesn't give like timestamp
#         if DATE_CUTOFF > favorite.created_at:
#             break
#         
#         print(favorite.user.screen_name)
#         print(favorite.user.name)
#         print(favorite.user.description)
# 
#         print(favorite.id)
#         print(favorite.text)
#         liked_by=angel
#         created_at=favorite.created_at
# 