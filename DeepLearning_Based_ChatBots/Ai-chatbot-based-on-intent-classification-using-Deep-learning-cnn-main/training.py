import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

import tensorflow as tf

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())

words = []  #for making vocabulary of words
classes = []
docs = []
ignoreLetters = ['?','!','.',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList)
        docs.append((wordList, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
outputEmpty = [0] * len(classes)


for document in docs:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    # The loop iterates over each word in the words list, which represents the vocabulary of unique words extracted from the input patterns.
    # For each word, it checks if that word is present in the current pattern (wordPatterns). 
    # If the word is present, it appends a 1 to the bag list; otherwise, it appends a 0. 
    # This process effectively creates a binary "bag of words" representation for each input pattern, 
    # where each element in the bag indicates whether a particular word from the vocabulary is present in the pattern or not.
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)

# EXPLAIATION::
#https://chat.openai.com/share/14c38bd0-2157-4434-a02d-c1d23146d3e5

random.shuffle(training)
training = np.array(training)

# training is something like: (input features + output labels) [1, 0, 1, 0, 1, 1, 0, 0]
# trainX contains the input features (bag of words representations) for all training examples. [1, 0, 1, 0, 1] | (bag of words representation)
# trainY contains the output labels (one-hot encoded intent classes) for all training examples.[1, 0, 0] | (one-hot encoded intent class)
trainX = training[:, :len(words)]
trainY = training[:, len(words):]

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5')
print('Done')

