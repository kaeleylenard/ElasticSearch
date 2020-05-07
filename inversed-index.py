import json
import os
from bs4 import BeautifulSoup
import re
import copy
import nltk
# nltk.download('punkt')
from nltk.stem import PorterStemmer

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
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(data)

    # removes words that shouldn't be considered
    copy_list = copy.deepcopy(tokens)
    for word in copy_list:
        if len(word) < 3:
            tokens.remove(word)
        else:
            # checks if stemming
            root_word = ps.stem(word)
            if word != root_word:
                tokens.remove(word)
                tokens.append(root_word)
    return tokens


def compute_tf(token, tokens):
    # term_freq(t,d) = count of t in d / number of words in d
    amount_of_token_in_tokens = tokens.count(token) * 1.0
    length_of_tokens = len(tokens) * 1.0
    return amount_of_token_in_tokens/length_of_tokens


def compute_idf():
    # inverse_doc_freq(t) = log(N/(df + 1))
    return 0.0


def compute_tfidf():
    # TO-DO: formula is tf-idf(t, d) = tf(t, d) * log(N/(df + 1))
    return 0.0


def add_to_index(document_words, docid_counter):
    # value should document name/id token was found in
    # and tf-idf score (need to compute)
    for word in document_words:
        tfidf_score = 0.0
        if word not in inverse_index:
            inverse_index[word] = set((docid_counter, tfidf_score))
        else:
            inverse_index.append((docid_counter, tfidf_score))


for subdir, dirs, files in os.walk(dev_directory):
    for file in files:
        docid_counter += 1
        json_file = os.path.join(subdir, file)
        alphanumeric_sequences = []
        print("current file:", json_file)
        try:
            soup = BeautifulSoup(open(json_file), 'html.parser')
            for text in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):
                data = text.get_text().strip()
                alphanumeric_sequences += tokenizes(data)
            add_to_index(alphanumeric_sequences, docid_counter)
        except Exception as e:
            print("error at:", e)


# for deliverable 1
deliverable_text = open('/Users/AreetaW/Desktop/deliverable.txt', 'w')
for key, value in inverse_index.items():
    deliverable_text.write(str(key) + ":     " + str(value) + "\n")
deliverable_text.close()


print("\nREPORT")
print("Number of documents:", docid_counter)
print("Number of unique tokens:", len(inverse_index))