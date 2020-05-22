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
            # add stemmed word to list
            rare_words.append(ps.stem(word))

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
    """

    queries_docs = []

    # Areeta
    final_text_index = "/Users/AreetaW/Desktop/final_text_index.txt"
    final_url_index = "/Users/AreetaW/Desktop/final_url_index.txt"
    dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV'
    # Kaeley
    # final_text_index = "/Users/kaeleylenard/Desktop/final_text_index.txt"
    # final_url_index = "/Users/kaeleylenard/Desktop/final_info_urls.txt"
    # dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/Assignment3/DEV'
    # Cristian
    # final_text_index = "/Users/kaeleylenard/Desktop/final_text_index.txt"
    # final_url_index = "/Users/kaeleylenard/Desktop/final_info_urls.txt"
    # dev_directory = 'C:\Test\DEV'
    # dev_directory = 'C:\Test\custom'

    # load dict of all urls in index
    with open(final_url_index) as url_file:
        url_response = json.loads(url_file.read())

    # load dict of inverted index
    with open(final_text_index) as text_file:
        text_response = json.loads(text_file.read())
        for (word, posting) in text_response['all_pages'].items():
            if word in rare_query:
                # add appearance of word in format: (word url, word, and td-idf score)

                # current issue: not able to eval posting because multiple sets
                list_of_postings = eval("[" + posting + "]")
                print(list_of_postings)
                for (docID, score) in list_of_postings:
                    url_path = dev_directory + url_response['0'][docID]
                    url_response = json.loads((open(url_path)).read())
                    queries_docs.append((url_response['url'], word, score))

    url_file.close()
    text_file.close()

    if len(queries_docs) > 1:
        return find_intersection(queries_docs)
    return queries_docs


def find_intersection(queries_docs):
    # HELLO I AM HAVING AN ISSUE DETERMINING HOW TO FIND INTERSECTIONS IF IT'S MULTIPLE WORDS
    # like if word has 3 urls and another word has 3 urls but only 1 match up
    intersections = 0
    while intersections < 4:
        for (word, url) in queries_docs.values():
            print("asdfsa")


def retrieval_component(query):
    """
    query: list of original query terms
    query_words: stemmed, rare query terms
    returned_docs: docs that contain ALL the query_words
    """
    rare_query = find_rare_words(query)
    returned_docs = iterate_info_files(rare_query)

    # print only the top five matches based on tf-idf score
    print(returned_docs.sort(key=lambda x: x[1], reverse=True)[0:5])


if __name__ == "__main__":
    user_query = input("Search: ")
    split_query = user_query.split()
    retrieval_component(split_query)