import os
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
from collections import defaultdict
import json
import time
import pandas
import math

# Kaeley:
# dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/Assignment3/DEV'
# Areeta:
# dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV'
# Cristian:
dev_directory = 'C:\Test\DEV'

inverse_index = dict()
docid_index = dict()
term_frequency = defaultdict(int)
docid_counter = 0
index_count = 0
word_count = 0
total_docs = 0
real_id = 0


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

        # determine if separated words b/c of punctuation
        if len(tokenized.split()) > 1:
            for token in tokenized.split():
                stemmed_word = ps.stem(token)
                if len(stemmed_word) >= 2:
                    tokens.append(stemmed_word)
        else:
            # determine if alphanumeric sequences
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
    # deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    # accompanying_text = open(f'/Users/kaeleylenard/Desktop/info_urls{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open(f'/Users/AreetaW/Desktop/info{index_count}.txt', 'w')
    # accompanying_text = open(f'/Users/AreetaW/Desktop/info_urls{index_count}.txt', 'w')
    # Cristian:
    deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')
    accompanying_text = open(f'C:\Test\info_urls{index_count}.txt', 'w')

    # writes to word indexer file
    with deliverable_text as json_file:
        # sorts dict by key
        inverse_index = {k: str(v) for k, v in sorted(inverse_index.items())}
        # pretty printing
        json.dump(inverse_index, json_file)
    deliverable_text.close()

    # writes to url indexer file
    with accompanying_text as index_json_file:
        # sorts dict by key
        docid_index = {k: v for k, v in sorted(docid_index.items())}
        # pretty printing
        json.dump(docid_index, index_json_file)
    accompanying_text.close()

    inverse_index.clear()
    docid_index.clear()


def add_to_index(document_words, docid_counter, real_id):
    # splits indexes into different files
    if docid_counter % 11000 == 0:
        write_to_file()

    # observes how many times a word shows up in a file
    for word in document_words:
        term_frequency[word] += 1

    # adds location id and tf_score for each word
    for word in document_words:
        term_freq = term_frequency[word]
        tf_score = 1 + math.log10(term_freq)
        doc_length = len(document_words)
       #print(word, tf_score, term_freq, dict_length)
        # decides whether word is unique or not
        if word not in inverse_index:
            first_appearance = (real_id, round(tf_score, 7), doc_length)
            inverse_index[word] = set()
            inverse_index[word].add(first_appearance)
        else:
            inverse_index[word].add((real_id, round(tf_score, 7), doc_length))

    # clears tf dict in order to prepare for next file
    term_frequency.clear()


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
    # accompanying_text = open(f'/Users/kaeleylenard/Desktop/info_urls{index_count}.txt', 'w')
    # Areeta:
    # deliverable_text = open(f'/Users/AreetaW/Desktop/info{index_count}.txt', 'w')
    # accompanying_text = open(f'/Users/AreetaW/Desktop/info_urls{index_count}.txt', 'w')
    # Cristian
    deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')
    accompanying_text = open(f'C:\Test\info_urls{index_count}.txt', 'w')

    # writes to word indexer file
    with deliverable_text as json_file:
       # print(inverse_index)
        inverse_index = {k: str(v) for k, v in sorted(inverse_index.items())}
        json.dump(inverse_index, json_file)
    deliverable_text.close()

    # writes to url indexer file
    with accompanying_text as index_json_file:
        docid_index = {k: v for k, v in sorted(docid_index.items())}
        json.dump(docid_index, index_json_file)
    accompanying_text.close()

    # Kaeley:
    # file_list = [f'/Users/kaeleylenard/Desktop/info{x+1}.txt' for x in range(index_count)]
    # url_list = [f'/Users/kaeleylenard/Desktop/info_urls{x+1}.txt' for x in range(index_count)]
    # Areeta:
    # file_list = [f'/Users/AreetaW/Desktop/info{x+1}.txt' for x in range(index_count)]
    # url_list = [f'/Users/AreetaW/Desktop/info_urls{x+1}.txt' for x in range(index_count)]
    # Cristian:
    file_list = [f'C:\Test\info{x + 1}.txt' for x in range(index_count)]
    url_list = [f'C:\Test\info_urls{x + 1}.txt' for x in range(index_count)]

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
    result['all_pages'] = result['all_pages'] = result["pages1"] + result["pages2"] + result["pages3"] + result["pages4"] + result["pages5"] + result["pages6"]

    for i in range(index_count):
        del result[f'pages{i + 1}']

    all_urls = []
    for urls in url_list:
        temps = pandas.read_json(urls, orient='index')
        all_urls.append(temps)

    url_result = pandas.concat(all_urls)

    # exports into excel and json file
    # Kaeley:
    # result.to_json(f'/Users/kaeleylenard/Desktop/final_text_index.txt')
    # result.to_json(f'/Users/kaeleylenard/Desktop/final_url_index.txt')
    # Areeta:
    # result.to_json(f'/Users/AreetaW/Desktop/final_text_index.txt')
    # url_result.to_json(f'/Users/AreetaW/Desktop/final_url_index.txt')
    # Cristian
    result.to_json("C:\Test\/final_text_index.txt")
    url_result.to_json("C:\Test\/final_url_index.txt")


def calculate_final_tf_idf(text_file, all_docs):
    final_indexer = {}
    with open(text_file, "r") as file:
        text_response = json.loads(file.read())

        # iterate through each word to update tf-idf score
        for word, posting in text_response['all_pages'].items():
            posts = re.sub('}{', ',', str(posting))
            posts = eval(posts)

            idf = round(math.log10(all_docs / len(posts)), 7)

            final_indexer[word] = idf

    # Kaeley:
    # tdidf_score_dict = open(f'', 'w')
    # Areeta:
    # tdidf_score_dict = open(f'/Users/AreetaW/Desktop/tf_idf_score_dict.txt', 'w')
    # Cristian:
    tdidf_score_dict = open("C:\Test\/tf_idf_score_dict.txt", 'w')

    # put final indexer with updated scores into new file
    with tdidf_score_dict as file:
        file.write(json.dumps(final_indexer))

    tdidf_score_dict.close()


def final_compile(text_file):
    compiled_index = "C:\Test\/compiled_index.txt"

    temp = pandas.read_json(text_file)
    temp.to_csv(compiled_index, chunksize=1000)

    line_index = dict()
    pos = 0
    with open(compiled_index) as indexed:
        for line in iter(indexed.readline, ''):
            word_term = re.findall(r'[A-Za-z0-9]+(?=,\"{)', line.split()[0])
            for i in word_term:
                line_index[i] = pos
            pos = indexed.tell()

    index_positions = "C:\Test\/index_positions.txt"
    with index_positions as shortcuts:
        shortcuts.write(json.dumps(line_index))


if __name__ == "__main__":
    # tracks time taken to complete indexing
    start_time = time.time()

    # loops through all files in DEV
    for subdir, dirs, files in os.walk(dev_directory):
        for file in files:
            json_file = os.path.join(subdir, file)
            docid_counter += 1
            real_id += 1
            alphanumeric_sequences = []
            print(f"current file {docid_counter} {index_count} {word_count} {real_id} :", json_file)

            # tokenizes all important text from each file and adds to index
            #try:
            soup = BeautifulSoup(open(json_file), 'html.parser')
            for text in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):
                # gets only text from each tag element
                data = text.get_text().strip()
                alphanumeric_sequences += tokenizes(data)

            # alphanumeric_sequences should be words of one json file
            add_to_index(alphanumeric_sequences, docid_counter, real_id)

            # uncomment this to your own length to remove subdirectories
            docid_index[real_id] = json_file[14:]

            #except Exception as e:
                #print("error at:", e)

    partial_indexing()

    # Kaeley:
    # calculate_final_tf_idf(f'/Users/kaeleylenard/Desktop/final_text_index.txt')
    # Areeta:
    # calculate_final_tf_idf(f'/Users/AreetaW/Desktop/final_text_index.txt')
    # Cristian
    calculate_final_tf_idf("C:\Test\/final_text_index.txt", total_docs)
    final_compile("C:\Test\/final_text_index.txt")

    # statistics
    print("\nREPORT")
    print("Number of Indexed Documents:", total_docs, " ", real_id)
    print("Number of Unique Words:", word_count)
    print("--- %s seconds ---" % (time.time() - start_time))
