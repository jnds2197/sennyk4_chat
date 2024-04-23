import keys
import tweepy
import socket
from emoji import demojize

def main():
    #V2 authentication, for text tweets
    client = tweepy.Client(
                consumer_key=keys.twitter_api_key,
                consumer_secret=keys.twitter_api_key_secret,
                access_token=keys.twitter_access_token,
                access_token_secret=keys.twitter_access_token_secret
            )

    #V1, for tweeting with images
    """
    auth = tweepy.OAuth1UserHandler(
        keys.twitter_api_key,
        keys.twitter_api_key_secret,
        keys.twitter_access_token,
        keys.twitter_access_token_secret,
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)
    """

    #Socket connection to Twitch
    sock = socket.socket()

    sock.connect((keys.twitch_server, keys.twitch_port))

    sock.send(f"PASS {keys.twitch_token}\n".encode('utf-8'))
    sock.send(f"NICK {keys.twitch_nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {keys.twitch_channel}\n".encode('utf-8'))

    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s — %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        handlers=[logging.FileHandler('chat.log', encoding='utf-8')])
    """

    #Listener
    while True:
        response = sock.recv(2048).decode('utf-8')

        if response.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        elif len(response) > 0:
            #logging.info(demojize(resp))

            response = str(demojize(response)).rstrip()
            username = response.split(':')[1:][0].split('!')[0]

            if(username == "sennyk4"):
                message = response.split(':', 1)[1:][1]
                #print(username)
                #print(message)
                client.create_tweet(text = message)
                print("Tweeted successfully")

    """
    def tweet(message: str, image_path = None):
        if image_path:
            media = api.media_upload(image_path)
            client.create_tweet(text = message, media_ids=[media.media_id])
            print("Tweeted successfully")

        else:      
            client.create_tweet(text = message)
            print("Tweeted successfully")

    """


if __name__ == '__main__':
    main()
