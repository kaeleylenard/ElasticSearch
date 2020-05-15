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
            # stem the word
            rare_words.append(ps.stem(word))
    return rare_words


def iterate_info_files(rare_query):
    """
    Find docs with the query terms.
    present_docs: docs that contain ALL the query terms
    rare_query: updated stemmed query with rare terms and no stop words
    """
    # list of dictionaries:
    # [{word: [docID, score]}
    present_docs = []

    # we have 6 info.txt files; edit this # if necessary
    for i in range(6):
        index_txt = open(f'/Users/kaeleylenard/Desktop/info{i}.txt', 'r')
        """
        Pseudocode because I don't have the completed index files yet:
        1. use a find method to search for a doc that contains all the terms in
        rare_query and then append it to the present_docs list
        2. sort present_docs from highest score to lowest score   
        """
    return present_docs


def retrieval_component(query):
    """
    query: list of original query terms
    query_words: stemmed, rare query terms
    returned_docs: docs that contain ALL the query_words
    """
    query_words = find_rare_words(query)
    returned_docs = iterate_info_files(query_words)

    # return only the top five matches
    for doc in returned_docs[:5]:
        # buffer the document to get the first line which contains the URL
        # print the URL
        print(doc)


if __name__ == "__main__":
    user_query = input("Search: ")
    split_query = user_query.split()
    retrieval_component(split_query)