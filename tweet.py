import dataset
import settings
db = dataset.connect(settings.CONNECTION_STRING)

#event-driven programming
import tweepy

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        
        if coords is not None:
            coords = json.dumps(coords)
        
        table = db[settings.TABLE_NAME]
        try:
            table.insert(dict(
            text=text,
            user_name=name,
            id_str=id_str,
            created=created,
            retweet_count=retweets,
            ))
        except ProgrammingError as err:
            print(err)
        
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)