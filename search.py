import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from collections import defaultdict
import math
import time

term_frequency = defaultdict(int)


def find_rare_words(query):
    """
    query: list of original query terms
    rare_words: list of query terms that are stemmed and not stop words
    """
    ps = PorterStemmer()

    return [ps.stem(word) for word in query]


def weigh_query(query):
    Scores = defaultdict(list)  # Holds score for all docs found
    Magnitude = defaultdict(int)  # Holds length of documents

    # query_norm = defaultdict(int) # Holds TF-IDF scores for query terms

    # Cristian
    # tdif_dict = "C:\Test\/tf_idf_score_dict.txt"

    # Kaeley
    tdif_dict = "/Users/kaeleylenard/Desktop/tf_idf_score_dict.txt"


    # Kaeley
    final_text_index = "/Users/kaeleylenard/Desktop/final_text_index.txt"
    final_url_index = "/Users/kaeleylenard/Desktop/final_url_index.txt"
    dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/SearchEngine/DEV'


    # Cristian
    # final_text_index = "C:\Test\/final_text_index.txt"
    # final_url_index = "C:\Test\/branch\/final_url_index.txt"
    # dev_directory = 'C:\Test\DEV\/'

    # load dict of all urls in index

    index_time = time.time()

    # load dict of inverted index

    with open(tdif_dict) as idf_scores:
        tfidf_response = json.loads(idf_scores.read())
    word_idf = [tfidf_response[v] for v in query]
    idf_scores.close()
    count = 0
    posts_time = time.time()
    with open(final_text_index) as text_file:
        text_responses = json.loads(text_file.read())
    print(f"--- posts {time.time() - posts_time} seconds ---")
    for word in query:
        if word in text_responses['all_pages']:

            posts = text_responses['all_pages'][word]
            posts = re.sub('}{', ',', str(posts))
            posts = eval(posts)

            term_idf = word_idf[count]
            count += 1
            for (docID, docTF, docLength) in posts:
                if docLength < 150:
                    pass
                else:
                    Scores[docID].append(([word, term_idf * docTF]))
                    Magnitude[docID] = docLength
                    # Magnitude[docID] = math.sqrt(docLength * docLength)
        else:
            print('not found')
            pass

    text_file.close()
    print(f"--- index  {time.time() - index_time} seconds ---")

    score_time = time.time()

    removal = [key for key in Scores if len(Scores[key]) < len(query)]
    for key in removal:
        del Scores[key]

    for k, v in Scores.items():
        Scores[k] = sum([float([v for v in group if type(v) == float][0]) for group in v])

    for doc in Scores:

        Scores[doc] = Scores[doc] / Magnitude[doc]

    print(f"--- score  {time.time() - score_time} seconds ---")
    five = [k for k, v in sorted(Scores.items(), key=lambda item: item[1], reverse=True)]

    final = []
    url_time = time.time()

    with open(final_url_index) as url_file:
        url_response = json.loads(url_file.read())
    for docID in five[:5]:
        url = url_response['0'][str(docID)]
        json_path = dev_directory + "/" + url_response['0'][str(docID)]
        json_path = re.sub("\\\\", "/", json_path)
        json_response = json.loads((open(json_path)).read())

        final.append(json_response['url'])
    print(f"--- url  {time.time() - url_time} seconds ---")
    print("--- %s seconds ---" % (time.time() - start_time))

    # PRINTING OUT SITES
    for i in final:
        print(i)

    url_file.close()

    return final


def retrieval_component(query):
    """
    query: list of original query terms
    query_words: stemmed, rare query terms
    returned_docs: docs that contain ALL the query_words
    """
    rare_time = time.time()
    rare_query = find_rare_words(query)
    print(f"--- rare {time.time() - rare_time} seconds ---")
    returned_docs = weigh_query(rare_query)
    return returned_docs
    # print only the top five matches based on tf-idf score
    # print(sorted(returned_docs, key=lambda x: x[1], reverse=True)[0:5])


if __name__ == "__main__":
    # user_query = input("Search: ")
    user_query = input("Search: ")
    start_time = time.time()
    split_query = user_query.split()
    retrieval_component(split_query)