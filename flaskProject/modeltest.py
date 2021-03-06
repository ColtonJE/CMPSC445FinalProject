import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import time
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from time import sleep
from tqdm import tqdm

import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

# set the labels for the dataset
Label_Columns = ["sentiment", "ids", "date", "flag", "user", "text"]

# read the csv file
dataset = pd.read_csv('training.1600000.processed.noemoticon.csv', encoding="ISO-8859-1", names=Label_Columns)

dataset.head()
dataset.info()
dataset['sentiment'].unique()
dataset = dataset[['sentiment', 'text']]
dataset['sentiment'] = dataset['sentiment'].replace(4, 1)
dataset['sentiment'].unique()

"""
Install stop words and word net
"""
# stop_words = nltk.download('stopwords')
# word_net = nltk.download('wordnet')


common_emoji = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad',
                ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
                ':-@': 'shocked', ':@': 'shocked', ':-$': 'confused', ':\\': 'annoyed',
                ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
                '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
                '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink',
                ';-)': 'wink', 'O:-)': 'angel', 'O*-)': 'angel', '(:-D': 'gossip', '=^.^=': 'cat'}

porter_stem = PorterStemmer()

sentiment, text = list(dataset['sentiment']), list(dataset['text'])


def preprocess(data_text):
    preprocessedd_text = []


    word_lemmatizer = nltk.WordNetLemmatizer()

    url_pattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    user_pattern = '@[^\s]+'
    alpha_pattern = "[^a-zA-Z0-9]"
    sequence_pattern = r"(.)\1\1+"
    seq_replace_pattern = r"\1\1"

    for tweet in data_text:
        tweet = tweet.lower()

        tweet = re.sub(url_pattern, ' ', tweet)

        for emoji in common_emoji.keys():
            tweet = tweet.replace(emoji, "EMOJI" + common_emoji[emoji])

        tweet = re.sub(user_pattern, " ", tweet)

        tweet = re.sub(alpha_pattern, " ", tweet)

        tweet = re.sub(sequence_pattern, seq_replace_pattern, tweet)

        tweet_words = ''

        for word in tweet.split():
            if word not in nltk.corpus.stopwords.words('english'):
                if len(word) > 1:
                    word = word_lemmatizer.lemmatize(word)
                    tweet_words += (word + ' ')
        preprocessedd_text.append(tweet_words)

        #show progress of preprocessing
        for i in tqdm(data_text):
            sleep(0.1)

    return preprocessedd_text


t = time.time()

# comment this section until the comment with "pickle complete"
# when model has been already trained and saved as a pickle file
#######################################################################################################################


# print(f'Starting Kaggle dataset text preprocessing.')
#
# preprocessed_text = preprocess(text)
#
# print(f'Kaggle dataset text preprocessing complete.')
# print(f'Completion time: {round(time.time() - t)} seconds')
#
# preprocessed_text[0:25]
#
# X_train, X_test, y_train, y_test = train_test_split(preprocessed_text, sentiment, test_size=0.05, random_state=0)
#
# tfid = TfidfVectorizer(ngram_range=(1, 2), max_features=500000)
# tfid.fit(X_train)
#
# X_train = tfid.transform(X_train)
# X_test = tfid.transform(X_test)
#
#
# def model_evaluate(model):
#     y_pred = model.predict(X_test)
#     print(classification_report(y_test, y_pred))
#     confusion_mtrx = confusion_matrix(y_test, y_pred)
#
#     categories = ['Negative', 'Positive']
#     group_names = ['True Negative', 'False Positive', 'False Negative', 'True Positive']
#     group_percentages = ['{0:.2%}'.format(value) for value in confusion_mtrx.flatten() / np.sum(confusion_mtrx)]
#     labels = [f'{v1}\n{v2}' for v1, v2 in zip(group_names, group_percentages)]
#     labels = np.asarray(labels).reshape(2, 2)
#
#     sns.heatmap(confusion_mtrx, annot=labels, cmap='Blues', fmt='', xticklabels=categories, yticklabels=categories)
#
#     plt.xlabel("Predicted values", fontdict={'size': 14}, labelpad=10)
#     plt.ylabel("Actual values", fontdict={'size': 14}, labelpad=10)
#     plt.title("Confusion Matrix", fontdict={'size': 18}, pad=20)
#
#
# t = time.time()
# model = LogisticRegression()
# model.fit(X_train, y_train)
# model_evaluate(model)
# print(f'Logistic Regression complete.')
# print(f'Time Taken: {round(time.time() - t)} seconds')
#
# file = open('vectoriser.pickle', 'wb')
# pickle.dump(tfid, file)
# file.close()
#
# file = open('logistic_regression.pickle', 'wb')
# pickle.dump(model, file)
# file.close()


#######################################################################################################################
# pickle complete
# comment until the line of #'s


def load_pickled_model():
    file = open('vectoriser.pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()

    file = open('logistic_regression.pickle', 'rb')
    log_model = pickle.load(file)
    file.close()

    return vectoriser, log_model


def predict(text):
    vectoriser, model = load_pickled_model()
    textdata = vectoriser.transform(preprocess(text))
    sentiment = model.predict(textdata)

    data = []
    for text, pred in zip(text, sentiment):
        data.append((text, pred))

    df = pd.DataFrame(data, columns=['text', 'sentiment'])
    df = df.replace([0, 1], ["Negative", "Positive"])
    print(df)
    return df.at[0, 'sentiment']