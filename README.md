# CS 121: Search Engine Project

This assignment's goal is to develop a a search engine from the ground up that is capable of handling tens of thousands of documents, under harsh operational constriants and having a query response time under 300ms.

## General specifications

Under the Algorithms and Data Structures Developer version, we created two separate programs: an indexer and a search component. Running the indexer across an entire entire collection of crawled pages, we were able to prompt the user for a query using a web GUI and respond with a list of URLs where the query appeared.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install nltk, BeautifulSoup, pandas, and Flask.

```bash
pip install --user -U nltk
pip install beautifulsoup4
pip install pandas
pip install Flask
```

## Usage

In order to run this program, run gui.py. Check to check if app is running, go to localhost:5000/.

## License
[MIT](https://choosealicense.com/licenses/mit/)
