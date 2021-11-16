from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import tweepy

digits = load_digits()

# Randomly split data into 70% training and 30% test
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=.30)

clf_KNN = KNeighborsClassifier()


def train():
    # Train a kNN model using the training set
    clf_KNN.fit(X_train, y_train)


def prediction():
    # Predictions using the kNN model on the test set
    print("Predicting labels of the test data set - %i random samples" % (len(X_test)))
    result = clf_KNN.predict(X_test)

    accuracy = 0
    return str(accuracy)

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
    text = status.full_text

    return text

def sentAnalysis( text ):
    import re
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer

    nltk.download('wordnet')

    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    lm = nltk.WordNetLemmatizer()
    review = [lm.lemmatize(word) for word in review]
    review = ' '.join(review)
    print(review)


    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    sent = sia.polarity_scores(review)
    print( sent )

    if( sent["neg"] > sent["pos"] ):
        return "Negative"
    elif( sent["pos"] > sent["neg"] ):
        return "Positive"
    # elif( sent["neu"] > sent["pos"] and sent["neu"] > sent["neg"] ):
    #     return "Neutral"
    else:
        return "Undeterminable"