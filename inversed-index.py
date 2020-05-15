import os
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import json
import time
import pandas

# Kaeley:
# dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/SearchEngine/DEV'
# Areeta:
# dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV'
# Cristian:
dev_directory = 'C:\Test\DEV'
# dev_directory = 'C:\Test\custom'


inverse_index = dict()
docid_index = dict()
docid_counter = 0
index_count = 0
word_count = 0
total_docs = 0
readl_id = 0


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
    global docid_index
    global inverse_index
    global word_count
    global docid_counter
    global total_docs

    word_count += len(inverse_index)
    total_docs += docid_counter
    index_count += 1
    docid_counter = 0

    # Kaeley:
    #deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open()
    # Cristian:
    deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')
    accompanying_text = open(f'C:\Test\info_urls{index_count}.txt', 'w')

    with accompanying_text as index_json_file:
        docid_index = {k: v for k, v in sorted(docid_index.items())}  # Sorts dict by key
        json.dump(docid_index, index_json_file)  # Pretty printing

    with deliverable_text as json_file:
        inverse_index = {k: list(v) for k, v in sorted(inverse_index.items())}  # Sorts dict by key
        json.dump(inverse_index, json_file)  # Pretty printing

    deliverable_text.close()
    accompanying_text.close()
    inverse_index.clear()
    docid_index.clear()


def add_to_index(document_words, docid_counter, real_id):
    """ The document_words variable stores the tokenized words in the current file """
    if docid_counter % 11000 == 0:
        write_to_file()
    tf_score = 0.0
    # adds each word to index with tf score
    for word in document_words:

        # calculates tf score for each word
        '''
        freq_of_token = float(document_words.count(word))
        amount_of_words = float(len(document_words))
        tf_score = freq_of_token/amount_of_words
        tf_score = round(tf_score, 5)
        '''

        # decides whether word is unique or not
        if word not in inverse_index:
            first_appearance = (real_id, tf_score)
            inverse_index[word] = set()
            inverse_index[word].add(first_appearance)

        else:
            inverse_index[word].add((real_id, tf_score))


def partial_indexing():
    global index_count
    global docid_index
    global inverse_index
    global word_count
    global docid_counter
    global total_docs

    # increments global information of index
    word_count += len(inverse_index)
    index_count += 1
    total_docs += docid_counter

    # Kaeley:
    # deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open()
    # Cristian
    deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')
    with deliverable_text as json_file:
        inverse_index = {k: list(v) for k, v in sorted(inverse_index.items())}
        json.dump(inverse_index, json_file)
    deliverable_text.close()

    accompanying_text = open(f'C:\Test\info_urls{index_count}.txt', 'w')
    with accompanying_text as index_json_file:
        docid_index = {k: v for k, v in sorted(docid_index.items())}  # Sorts dict by key
        json.dump(docid_index, index_json_file)  # Pretty printing
    accompanying_text.close()

    # Kaeley:
    # file_list = [f'/Users/kaeleylenard/Desktop/info{x+1}.txt' for x in range(index_count)]
    # Areeta:
    # file_list = []
    # Cristian:
    file_list = [f'C:\Test\info{x+1}.txt' for x in range(index_count)]
    url_list = [f'C:\Test\info_urls{x + 1}.txt' for x in range(index_count)]

    # pandas will merge all json files alphabetically
    bases = []
    for file in file_list:
        temp = pandas.read_json(file, orient='index')
        bases.append(temp)

    all_urls = []
    for urls in url_list:
        temps = pandas.read_json(urls,  orient='index')
        all_urls.append(temps)
    # holds all json files as one big pandas dataframe
    result = pandas.concat(bases)
    url_result = pandas.concat(all_urls)
    # exports into excel and json file
    # Kaeley:
    # result.to_csv()
    # Areeta:
    # result.to_csv("/Users/AreetaW/Desktop/finalindex.csv")
    # Cristian:
    #result.to_csv("C:\Test\/finalindex.csv")
    result.to_json("C:\Test\/finaltextindex.txt")
    url_result.to_json("C:\Test\/final_url_index.txt")


if __name__ == "__main__":
    # tracks time taken to complete indexing
    start_time = time.time()
    # loops through all files in DEV
    for subdir, dirs, files in os.walk(dev_directory):
        for file in files:
            json_file = os.path.join(subdir, file)
            docid_counter += 1
            readl_id += 1
            alphanumeric_sequences = []
            print(f"current file {docid_counter} {index_count} {word_count} {readl_id} :", json_file)

            # tokenizes all important text from each file and adds to index
            try:
                soup = BeautifulSoup(open(json_file), 'html.parser')
                for text in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):

                    # gets only text from each tag element
                    data = text.get_text().strip()
                    alphanumeric_sequences += tokenizes(data)
                add_to_index(alphanumeric_sequences, docid_counter, readl_id)
                docid_index[readl_id] = json_file[12:]

            except Exception as e:
                print("error at:", e)
    partial_indexing()

    # Statistics
    print("\nREPORT")
    print("Number of Indexed Documents:", total_docs, " ", readl_id)
    print("Number of Unique Words:", word_count)
    print("--- %s seconds ---" % (time.time() - start_time))