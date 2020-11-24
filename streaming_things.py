import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import socket
import json

SECRETS = json.load(open('secrets.json','r'))
consumer_key = SECRETS['consumer_key']
consumer_secret = SECRETS['consumer_secret']
access_token = SECRETS['access_token']
access_secret = SECRETS['access_secret']

class TweetListener(StreamListener):
    """
    Listens for data on a connection/socket. 
    """
    
    def __init__(self, csocket):
        """
        Initializes a connection.
        """
        self.client_socket = csocket
        
    def on_data(self, data):
        """
        Loads data as JSON, grabs text, and sends text through socket.
        """
        
        try:
            msg = json.loads(data)
            print(msg['text'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print('ERROR:',e)
        return True
    
    def on_error(self, status):
        """
        """
        print(status)
        return True

def sendData(c_socket):
    """
    Connects to Twitter, launches stream, and filters for given track(s). 
    """
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth, TweetListener(c_socket))
    twitter_stream.filter(track=['Litecoin']) # enter topics to listen for here

if __name__ == '__main__':
    s = socket.socket()
    host = '127.0.0.1'
    port = 5555
    s.bind((host,port))
    
    print(f'Listening on port: {port}')
    
    s.listen(5)
    c,addr = s.accept()
    
    sendData(c)