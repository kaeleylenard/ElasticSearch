import json
from nltk.stem import PorterStemmer
import re
from collections import defaultdict
import math
import time

term_frequency = defaultdict(int)


def stem_words(query):
    """
    query: list of original query terms
    return: list of stemmed query terms
    """
    ps = PorterStemmer()
    return [(ps.stem(word)) for word in query]


def iterate_info_files(stemmed_query):
    """
    Find docs with the query terms.
    present_docs: docs that contain ALL the query terms
    rare_query: updated stemmed query with rare terms and no stop words
    """

    queries_docs = []

    # Areeta
    #final_text_index = "/Users/AreetaW/Desktop/final_text_index.txt"
    #final_url_index = "/Users/AreetaW/Desktop/final_url_index.txt"
    #dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV/'
    # Kaeley
    # final_text_index = "/Users/kaeleylenard/Desktop/final_text_index.txt"
    # final_url_index = "/Users/kaeleylenard/Desktop/final_url_index.txt"
    # dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/SearchEngine/DEV'
    # Cristian
    final_text_index = "C:\Test\/areeta\/final_text_index.txt"
    final_url_index = "C:\Test\/areeta\/final_url_index.txt"
    dev_directory = 'C:\Test\DEV'
    # dev_directory = 'C:\Test\custom'

    # load dict of all urls in index
    with open(final_url_index) as url_file:
        url_response = json.loads(url_file.read())

    # load dict of inverted index
    with open(final_text_index) as text_file:
        text_response = json.loads(text_file.read())

        for word in stemmed_query:
            results = text_response['all_pages'][word]
            posts = re.sub('}{', ', ', str(results))
            posts = eval(posts)
            #posts = re.sub('}', '}, ', str(results))
            #posts = eval(posts)[0]

            posts = sorted(posts, key=lambda tup: tup[1], reverse=True)[:10]
            #print(posts)
            for (docID, score) in posts:

                json_path = dev_directory + "/" + url_response['0'][str(docID)]
                #print(url_response['0'][str(docID)])
                # {'url': 'https://blablabla', 'content':}
                json_response = json.loads((open(json_path)).read())

                # queries_docs.append((docID, score))
                queries_docs.append(json_response['url'])

    url_file.close()
    text_file.close()
    return queries_docs


def weigh_query(query):
    """ Getting and printing information about each query term """
    for word in query:
        term_frequency[word] += 1

    # adds location id and tf_score for each word
    for word in query:
        term_freq = term_frequency[word]
        tf_score = 1 + math.log10(term_freq)
        dict_length = len(term_frequency)
        # idf score: log(amount of unique words / how many times words appear)
        idf = math.log10(dict_length / term_freq)

        # Testing:
        # print(f'word:{word}, tf_score:{tf_score}, unique_words:{dict_length}, idf:{idf}')


def retrieval_component(query):
    """
    query: list of original query terms
    query_words: stemmed, rare query terms
    returned_docs: docs that contain ALL the query_words
    """
    #weigh_query(query)
    returned_docs = iterate_info_files(query)

    # print only the top five matches based on tf-idf score
    # print(sorted(returned_docs, key=lambda x: x[1], reverse=True)[0:5])
    print("--- %s seconds ---" % (time.time() - start_time))
    for site in sorted(returned_docs, key=lambda x: x[1], reverse=True)[0:5]:
        print(site)


if __name__ == "__main__":
    # user_query = input("Search: ")
    print('Search')
    user_query = input("Search: ")
    start_time = time.time()
    split_query = user_query.split()
    print(split_query)
    # stem query terms to match with final indices
    retrieval_component(stem_words(split_query))

