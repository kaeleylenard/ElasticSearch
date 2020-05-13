import os
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import json
import time
import demjson
import pandas

# Kaeley:
dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/SearchEngine/DEV'
# Areeta:
# dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV'
# Cristian:
# dev_directory = 'C:\Test\DEV'
# dev_directory = 'C:\Test\custom'


inverse_index = dict()
docid_counter = 0
index_count = 0
word_count = 0
total_docs = 0


def tokenizes(data):
    """ Tokenizes the words in a tag """
    data = data.split()  # split sentence into words
    tokens = list()
    ps = PorterStemmer()

    for word in data:
        tokenized = re.sub('[^A-Za-z0-9]+', ' ', str(word))
        if len(tokenized) >= 2:
            tokens.append(ps.stem(tokenized))
    return tokens


def write_to_file():
    global index_count
    global inverse_index
    global word_count
    global docid_counter
    global total_docs

    word_count += len(inverse_index)
    total_docs += docid_counter
    index_count += 1
    docid_counter = 0

    # Kaeley:
    deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open()
    # Cristian:
    # deliverable_text = open()

    with deliverable_text as json_file:
        json.dump(demjson.encode(inverse_index), json_file)
    deliverable_text.close()
    inverse_index.clear()


def add_to_index(document_words, docid_counter):
    """ The document_words variable sttores the tokenized words in the current file """
    if docid_counter % 11000 == 0:
        write_to_file()

    for word in document_words:
        tfidf_score = 0.0
        if word not in inverse_index:
            first_appearance = (docid_counter, tfidf_score)
            inverse_index[word] = set()  # Now works with aid of demjson package
            inverse_index[word].add(first_appearance)
        else:
            inverse_index[word].add((docid_counter, tfidf_score))


def partial_indexing():
    global index_count
    global inverse_index
    global word_count
    global docid_counter
    global total_docs

    word_count += len(inverse_index)
    index_count += 1
    total_docs += docid_counter

    # Kaeley:
    deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open()
    # Cristian:
    # deliverable_text = open()

    with deliverable_text as json_file:
        json.dump(demjson.encode(inverse_index), json_file)
    deliverable_text.close()

    # Kaeley:
    file_list = [f'/Users/kaeleylenard/Desktop/info{x+1}.txt' for x in range(index_count)]
    # Areeta:
    # file_list = []
    # Cristian:
    # file_list - []

    # Kaeley:
    with open('/Users/kaeleylenard/Desktop/data.txt', 'w') as json_file:
        for index in file_list:
            with open(index) as file:
                data = json.load(file)
                data = demjson.decode(data)
                json.dump(data, json_file)

#bases = []  # Use of pandas to merge all json files alphabetically
    #for file in file_list:
        #temp = pandas.read_json(file, orient='index')
        #bases.append(temp)
    #result = pandas.concat(bases)  # This should hold all json files as one big pandas dataframe
    ## result.to_csv("C:\Test\/finalindex.csv")  # This will export it into excel


if __name__ == "__main__":
    start_time = time.time()
    for subdir, dirs, files in os.walk(dev_directory):
        for file in files:
            json_file = os.path.join(subdir, file)
            docid_counter += 1
            alphanumeric_sequences = []
            print(f"current file {docid_counter} {index_count} {word_count} :", json_file)
            try:
                soup = BeautifulSoup(open(json_file), 'html.parser')
                for text in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):
                    data = text.get_text().strip()  # text in the tag
                    alphanumeric_sequences += tokenizes(data)
                add_to_index(alphanumeric_sequences, docid_counter)
            except Exception as e:
                print("error at:", e)
    partial_indexing()

    # Statistics
    print("\nREPORT")
    print("Number of Indexed Documents:", total_docs)
    print("Number of Unique Words:", word_count)
    print("--- %s seconds ---" % (time.time() - start_time))