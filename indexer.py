from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import json
import time
import pandas
import os
import pickle

# Kaeley:
dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/Assignment3/DEV/seal_ics_uci_edu'
# Areeta:
# dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV'
# Cristian:
# dev_directory = 'C:\Test\DEV'
# dev_directory = 'C:\Test\custom'


inverse_index = dict()
docid_index = dict()
docid_counter = 0
index_count = 0
word_count = 0
total_docs = 0
readl_id = 0


def tokenizes(data):
    # splits tags into words in a list
    data = data.split()
    tokens = list()
    ps = PorterStemmer()
    tokenized = ''

    for word in data:
        # remove punctuation
        tokenized = re.sub('[^A-Za-z0-9]+', ' ', str(word))
        tokenized = re.sub('_', ' ', str(tokenized))
        tokenized = tokenized.strip()

        # determine if separated words
        if len(tokenized.split()) > 1:
            for token in tokenized.split():
                stemmed_word = ps.stem(token)
                if len(stemmed_word) >= 2:
                    tokens.append(stemmed_word)
        else:
            if len(ps.stem(tokenized)) >= 2:
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
    deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    accompanying_text = open(f'/Users/kaeleylenard/Desktop/info_urls{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open(f'/Users/AreetaW/Desktop/info{index_count}.txt', 'w')
    # accompanying_text = open(f'/Users/AreetaW/Desktop/info_urls{index_count}.txt', 'w')
    # Cristian:
    # deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')
    # accompanying_text = open(f'C:\Test\info_urls{index_count}.txt', 'w')

    with accompanying_text as index_json_file:
        # sorts dict by key
        docid_index = {k: v for k, v in sorted(docid_index.items())}
        json.dump(docid_index, index_json_file)
    accompanying_text.close()

    with deliverable_text as json_file:
        # sorts dict by key
        inverse_index = {k: str(v) for k, v in sorted(inverse_index.items())}
        # pretty printing
        json.dump(inverse_index, json_file)
    deliverable_text.close()

    inverse_index.clear()
    docid_index.clear()


def add_to_index(document_words, docid_counter, real_id):
    # splits indexes into different files
    if docid_counter % 11000 == 0:
        write_to_file()

    for word in document_words:
        tf_score = document_words.count(word) / len(document_words)
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
    deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    accompanying_text = open(f'/Users/kaeleylenard/Desktop/info_urls{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open(f'/Users/AreetaW/Desktop/info{index_count}.txt', 'w')
    # accompanying_text = open(f'/Users/AreetaW/Desktop/info_urls{index_count}.txt', 'w')
    # Cristian
    # deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')
    # accompanying_text = open(f'C:\Test\info_urls{index_count}.txt', 'w')

    with deliverable_text as json_file:
        inverse_index = {k: str(v) for k, v in sorted(inverse_index.items())}
        json.dump(inverse_index, json_file)
    deliverable_text.close()

    with accompanying_text as index_json_file:
        docid_index = {k: v for k, v in sorted(docid_index.items())}
        json.dump(docid_index, index_json_file)
    accompanying_text.close()

    # Kaeley:
    file_list = [f'/Users/kaeleylenard/Desktop/info{x+1}.txt' for x in range(index_count)]
    url_list = [f'/Users/kaeleylenard/Desktop/info_urls{x+1}.txt' for x in range(index_count)]
    # Areeta:
    # file_list = [f'/Users/AreetaW/Desktop/info{x+1}.txt' for x in range(index_count)]
    # url_list = [f'/Users/AreetaW/Desktop/info_urls{x+1}.txt' for x in range(index_count)]
    # Cristian:
    # file_list = [f'C:\Test\info{x + 1}.txt' for x in range(index_count)]
    # url_list = [f'C:\Test\info_urls{x + 1}.txt' for x in range(index_count)]

    # pandas will merge all json files alphabetically
    bases = []
    for file in file_list:
        temp = pandas.read_json(file, orient='index')
        bases.append(temp)

    result = bases[0]
    result.columns = ['pages1']
    count = 2
    for i in bases[1:]:
        i.columns = [f'pages{count}']
        count += 1
        result = result.join(i, how='outer', lsuffix="_left", rsuffix="_right")
    result = result.fillna('')
    # result['all_pages'] = result["pages1"] + result["pages2"] + result["pages3"] + result["pages4"] + result["pages5"] + result["pages6"]
    result['all_pages'] = result["pages1"]
    for i in range(index_count):
        del result[f'pages{i + 1}']

    all_urls = []
    for urls in url_list:
        temps = pandas.read_json(urls, orient='index')
        all_urls.append(temps)

    url_result = pandas.concat(all_urls)

    # exports into excel and json file
    # Kaeley:
    result.to_json(f'/Users/kaeleylenard/Desktop/final_text_index.txt')
    result.to_json(f'/Users/kaeleylenard/Desktop/final_url_index.txt')
    # Areeta:
    # result.to_json(f'/Users/AreetaW/Desktop/final_text_index.txt')
    # url_result.to_json(f'/Users/AreetaW/Desktop/final_url_index.txt')
    # Cristian
    # result.to_json("C:\Test\/finaltextindex.txt")
    # url_result.to_json("C:\Test\/final_url_index.txt")


def final_tfidf(txtfile):
    new_file = open("/Users/kaeleylenard/Desktop/tdidf_scores.pkl", "wb")

    finaltextdict = {}
    with open(txtfile) as file:
        text_response = json.loads(file.read())
        for word, posting in text_response['all_pages'].items():
            posting = eval(posting)
            new_postings = set()
            for docID, tfscore in posting:
                idf = len(posting) / 2027  # 2027 = number of words in sample im using
                new_postings.add((docID, tfscore*idf))
            finaltextdict[word] = new_postings

    pickle.dump(finaltextdict, new_file)
    # Checking and printing full dict with complete tdidf scores
    new_file = open("/Users/kaeleylenard/Desktop/tdidf_scores.pkl", "rb")
    output = pickle.load(new_file)
    print(output)


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

                # new edit: added length of tokenizes(data) to calculate tf
                add_to_index(alphanumeric_sequences, docid_counter, readl_id)

                # uncomment this to your own length to remove subdirectories
                docid_index[readl_id] = json_file[49:]

            except Exception as e:
                print("error at:", e)
    partial_indexing()
    final_tfidf("/Users/kaeleylenard/Desktop/final_text_index.txt")

    # Statistics
    print("\nREPORT")
    print("Number of Indexed Documents:", total_docs, " ", readl_id)
    print("Number of Unique Words:", word_count)
    print("--- %s seconds ---" % (time.time() - start_time))
