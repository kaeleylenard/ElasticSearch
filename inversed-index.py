import json
import os
from bs4 import BeautifulSoup
import re

# UNCOMMENTT THIS BASED ON WHO'S COMPUTER IS BEING USED

# Kaeley:
dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/Assignment3/DEV'

# Areeta:
# dev_directory = ''

# Cristian:
# dev_directory = ''

# to check:
# print(os.path.exists(dev_directory))

inverse_index = dict()
docid_counter = 0  # for naming docID


def tokenizer(data):
    """ Takes in a string and returns a set of valid alphanumeric sequences """
    data = data.split()
    word_set = set()

    for word in data:
        if word.isalpha() and len(word) > 1:
            word_set.add(word.lower())

        else:
            """ Words that contain a non-alphanumeric character are
            split and counted into individual sequences. """

            non_alpha = ""
            for letter in word:
                if not letter.isalnum():
                    non_alpha = letter

            if non_alpha != "": #A nonalphanumeric char is present
                split_word = word.split(non_alpha)

                # Handling hyphens, apostrophes, and end punctuation
                if non_alpha in "-'.,!?:;()[]{}*":
                    for fragment in split_word:
                        # The fragment must be an alphanumeric sequence
                        if len(fragment) > 1 and fragment.isalpha():
                            word_set.add(fragment.lower())

    return word_set


def add_to_index(words, ID):
    # 0.000 = tf-idf score (need to compute)
    for word in words:
        if word not in inverse_index:
            inverse_index[word] = [{ID: "0.000"}]
        else:
            inverse_index[word].append({ID: "0.000"})


def get_docname(counter):
    return "doc" + str(counter)


for subdir, dirs, files in os.walk(dev_directory):
    for file in files:
        docid_counter += 1
        document_words = set()
        json_file = os.path.join(subdir, file)

        try:
            soup = BeautifulSoup(open(json_file), 'html.parser')
            for text in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):
                data = text.get_text().strip()
                alphanumeric_sequences = tokenizer(data)  # set - no duplicates]
                document_words |= alphanumeric_sequences

            doc_id = get_docname(docid_counter)
            add_to_index(document_words, doc_id)
            print("current file:", json_file)
        except:
            print("error at", json_file)

# Organize this in a table for submission
#for key, value in inverse_index.items():
#    print(key, value)

print("\nREPORT")
print("Number of documents:", docid_counter)
print("Number of unique tokens:", len(inverse_index))





