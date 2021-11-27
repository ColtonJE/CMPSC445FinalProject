import tweepy

def tweetText(url):

    # Opens file that contains Twitter Developer License Keys
    licenseFile = open('license.txt', 'r')

    # Assigns token to its respective key
    consumerKey = licenseFile.readline().rstrip()
    secretConsumeKey = licenseFile.readline().rstrip()
    accessToken = licenseFile.readline().rstrip()
    secretAccessToken = licenseFile.readline().rstrip()

    # Sets up authorization
    auth = tweepy.OAuthHandler(consumerKey, secretConsumeKey)
    auth.set_access_token(accessToken, secretAccessToken)
    api = tweepy.API(auth)

    # Gets Tweet status ID from the URL
    id = url.split('/')[-1]

    # Pulls text from the tweet
    # Tweepy defaults to 140 characters, but Twitter allows 280 characters. tweet_mode matches Twitter character limit
    status = api.get_status(id, tweet_mode="extended")

    # Retweets do not have extended attribute status, and will throw an AttributeError when sending as a string
    try:
        text = status.full_text
    except AttributeError:
        text = status.retweeted_status.full_text

    return text
