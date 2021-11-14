from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

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