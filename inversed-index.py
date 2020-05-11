import json
import os
from bs4 import BeautifulSoup
import re
import copy
import nltk
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
from nltk.stem import PorterStemmer
import math

# UNCOMMENT THIS BASED ON WHOSE COMPUTER IS BEING USED

# Kaeley:
#dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/Assignment3/DEV'

# Areeta:
dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV'

# Cristian:
# dev_directory = ''

# to check:
# print(os.path.exists(dev_directory))

inverse_index = dict()
docid_counter = 0  # for naming docID


def tokenizes(data):
    # tokenizes and stems with ntlk
    ps = PorterStemmer()
    tokens = word_tokenize(data)

    # removes words that shouldn't be considered
    copy_list = copy.deepcopy(tokens)
    for word in copy_list:
        if len(word) < 2:
            tokens.remove(word)
        else:
            # checks if stemming
            root_word = ps.stem(word)
            if word != root_word:
                tokens.remove(word)
                tokens.append(root_word)
    return tokens


def add_to_index(document_words, docid_counter):
    # value should document name/id token was found in

    for word in document_words:
        # calculate tf score, freq of token in an entire doc
        freq_of_token = float(document_words.count(word))
        amount_of_words = float(len(document_words))
        tf_score = freq_of_token/amount_of_words

        if word not in inverse_index:
            first_appearance = (docid_counter, tf_score)
            inverse_index[word] = set()
            inverse_index[word].add(first_appearance)
        else:
            inverse_index[word].add((docid_counter, tf_score))


for subdir, dirs, files in os.walk(dev_directory):
    for file in files:
        docid_counter += 1
        json_file = os.path.join(subdir, file)
        alphanumeric_sequences = []
        print("current file:", json_file)
        try:
            soup = BeautifulSoup(open(json_file), 'html.parser')
            for text in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):
                data = text.get_text(" ", strip=True)
                data = data.lower()
                data = re.sub('[^A-Za-z0-9]+', ' ', str(data))
                alphanumeric_sequences += tokenizes(data)
            add_to_index(alphanumeric_sequences, docid_counter)
        except Exception as e:
            print("error at:", e)


# for deliverable 1
deliverable_text = open('/Users/AreetaW/Desktop/deliverable.txt', 'w')
for key, value in inverse_index.items():
    # find inverse of (total number of docs/number of docs with token in it)
    for v in value:
        v[1] *= math.log(float(docid_counter)/float(len(inverse_index[key])))
    deliverable_text.write(str(key) + ":     " + str(value) + "\n")
deliverable_text.close()


print("\nREPORT")
print("Number of Indexed Documents:", docid_counter)
print("Number of Unique Words:", len(inverse_index))