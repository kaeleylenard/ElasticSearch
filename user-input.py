import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def find_rare_words(query):
    """
    query: list of original query terms
    rare_words: list of query terms that are stemmed and not stop words
    """
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    rare_words = list()

    for word in query:
        if word not in stop_words:
            rare_words.append(ps.stem(word))  # stem the word

    # for queries that contain only stopwords, such as "to be or not to be"
    # just return the entire query - will need to find documents that contain
    # the exact amount of stopwords in the query (assumption)
    if len(rare_words) == 0:
        return query
    return rare_words


def iterate_info_files(rare_query):
    """
    Find docs with the query terms.
    present_docs: docs that contain ALL the query terms
    rare_query: updated stemmed query with rare terms and no stop words

    posting:
    word : “{(docID, score)}”

    entire file:
    {“0”: {word : “{(docID, score)}”}}
    """

    present_docs = []  # holds all curr docs that match the words
    found = 0

    # Areeta
    # final_text_index = "/Users/AreetaW/Desktop/finaltextindex.txt"
    # Kaeley
    final_text_index = "/Users/kaeleylenard/Desktop/final_text_index.txt"
    final_url_index = "/Users/kaeleylenard/Desktop/info_urls1.txt"
    with open(final_url_index) as file:
        url_response = json.loads(file.read())
    # Cristian
    # final_text_index = ''

    with open(final_text_index) as file:
        text_response = json.loads(file.read())
        # format for postings {(docID, score)} is a string
        for (word, posting) in text_response['0'].items():
            if word in rare_query:
                for (docID, score) in eval(posting):
                    for(ID, json_file) in url_response.items():
                        print(json_file)
                        # next steps: get url from json file, ranking, MAKE THIS MORE EFFICIENT AAAH
"""
# Areeta's:

with open("/Users/AreetaW/Desktop/finaltextindex.txt") as file:
    response = json.loads(file.read())
    for (word, postings) in response['0'].items():
        if rare_words[found] == word:
            found += 1
            # took out quotes and curly brackets on both sides 
            # need to figure out how to unstringify it
            posting_info = posting_info[1:-1]
            
            # add posting_info to present docs
"""


def retrieval_component(query):
    """
    query: list of original query terms
    query_words: stemmed, rare query terms
    returned_docs: docs that contain ALL the query_words
    """
    query_words = find_rare_words(query)
    returned_docs = iterate_info_files(query_words)

    # return only the top five matches
    # for doc in returned_docs[:5]:
        # buffer the document to get the first line which contains the URL
        # print the URL
        # print(doc)


if __name__ == "__main__":
    user_query = input("Search: ")
    split_query = user_query.split()
    retrieval_component(split_query)