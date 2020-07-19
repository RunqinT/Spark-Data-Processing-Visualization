import socket
import sys
import requests
import requests_oauthlib
import json

# Replace the values below with yours Access Token
TWITTER_ACCESS_TOKEN = '1063944351724662784-MVTRTpJk2JdoFTOl3UeVt04orBjSUJ'
TWITTER_ACCESS_SECRET = 'GgwSxgkQVrXfnsQXxbuon3CDmV9GERKz0H8EYfv3Db76p'
TWITTER_CONSUMER_KEY = 'EL9bP53IKTBWsmNVkXeBaTLH0'
TWITTER_CONSUMER_SECRET = 'URuSzNfTCFBq7nPyaSqAjqksECbD2vUFUMq2RfhYSjoloWPQbq'
twitter_auth = requests_oauthlib.OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET) 

def streamTweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    # query_data = [('language', 'en'), ('locations', '-122,-37,-122,38'),('track','#')]
    stream_param = [('language', 'en'), ('locations', '-90,-20,100,50'), ('track', '#')]
    stream_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in stream_param])
    resp = requests.get(stream_url, auth=twitter_auth, stream=True)
    print(stream_url, resp)
    return resp

def twitter_to_spark(resp, tcp_conn):
    for line in resp.iter_lines():
        try:
            whole_tweet = json.loads(line)
            tweet_pure_text = whole_tweet['text'] + '\n'      # pyspark can't accept stream, add '\n'

            print("Tweet pure text is : " + tweet_pure_text)
            print ("------------------------------------------")
            tcp_conn.send(tweet_pure_text.encode('utf-8', errors='ignore'))
        except:
            e = sys.exc_info()[0]
            print("Error is: %s" % e)


conn = None
TCP_IP = "localhost"
TCP_PORT = 9090
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)
print("Twitter end server is waiting for Spark Process connection...")
conn, addr = sock.accept()
print("Spark process is connected and streaming tweets to Spark process.")
resp = streamTweets()
twitter_to_spark(resp,conn)
