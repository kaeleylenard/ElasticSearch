import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from collections import defaultdict
import math
import time

term_frequency = defaultdict(int)


def stem_words(query):
    """
    query: list of original query terms
    rare_words: list of query terms that are stemmed and not stop words
    """
    ps = PorterStemmer()

    return [ps.stem(word) for word in query]


def weigh_query(query):
    Scores = defaultdict(list)  # Holds score for all docs found
    Magnitude = defaultdict(int)  # Holds length of documents

    tdif_dict = "C:\Test\/tf_idf_score_dict.txt"

    # Areeta
    # final_text_index = "/Users/AreetaW/Desktop/final_text_index.txt"
    # final_url_index = "/Users/AreetaW/Desktop/final_url_index.txt"
    # dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV/'
    # Kaeley
    # final_text_index = "/Users/kaeleylenard/Desktop/final_text_index.txt"
    # final_url_index = "/Users/kaeleylenard/Desktop/final_url_index.txt"
    # dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/SearchEngine/DEV'
    # Cristian
    final_url_index = "C:\Test\/branch\/final_url_index.txt"
    dev_directory = 'C:\Test\DEV\/'
    index_positions = "C:\Test\/index_positions.txt"
    compiled_index = "C:\Test\/compiled_text_index.txt"

    # Load file with idf scores for cosine
    with open(tdif_dict) as idf_scores:
        tfidf_response = json.loads(idf_scores.read())

    # Load file with positions of word lines in compiled_index
    with open(index_positions) as index_file:
        index_responses = json.loads(index_file.read())

    # Have address of compiled text
    text_file = open(compiled_index)

    for word in query:
        if word in index_responses:
            pos = index_responses[word]
            text_file.seek(pos)
            posts = text_file.readline()
            posts = re.sub(f'{word},"', '', str(posts))
            posts = re.sub(f'"', '', str(posts))
            posts = re.sub('}{', ',', str(posts))
            posts = eval(posts)

            term_idf = tfidf_response[word]
            for (docID, docTF, docLength) in posts:
                if docLength < 150:
                    pass
                else:
                    Scores[docID].append(([word, term_idf * docTF]))
                    Magnitude[docID] = docLength
        else:
            pass

    text_file.close()
    idf_scores.close()

    # Ensure found documents have all query terms
    query_length_check = [key for key in Scores if len(Scores[key]) < len(query)]
    for key in query_length_check:
        del Scores[key]

    # Combine scores from each individual query term into final doc score
    for k, v in Scores.items():
        Scores[k] = sum([float([v for v in group if type(v) == float][0]) for group in v])

    # Attempt to normalize by diving by length of document
    for doc in Scores:
        Scores[doc] = Scores[doc] / Magnitude[doc]

    # Get top 5 from scores by ranking by cosine score
    five = [k for k, v in sorted(Scores.items(), key=lambda item: item[1], reverse=True)]

    final = []

    # Load file with urls attached to json file name
    with open(final_url_index) as url_file:
        url_response = json.loads(url_file.read())
    for docID in five[:5]:
        url = url_response['0'][str(docID)]
        json_path = dev_directory + url_response['0'][str(docID)]
        json_response = json.loads((open(json_path)).read())
        final.append(json_response['url'])
    url_file.close()
    print(f"--- time  {time.time() - start_time} seconds ---")
    return final


def retrieval_component(query):
    """
    query: list of original query terms
    query_words: stemmed, rare query terms
    returned_docs: docs that contain ALL the query_words
    """
    rare_query = stem_words(query)

    returned_docs = weigh_query(rare_query)
    for links in returned_docs:
        print(links)


if __name__ == "__main__":
    user_query = input("Search: ")
    start_time = time.time()
    split_query = user_query.split()
    retrieval_component(split_query)