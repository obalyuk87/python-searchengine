import os.path
from download import download_wikipedia_abstracts
from load import load_documents
from search.timing import timing
from search.index import Index
import cache
from pprint import pprint

@timing
def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index


if __name__ == '__main__':
    ######################################################################################################
    # this will only download the xml dump if you don't have a copy already;
    # just delete the file if you want a fresh copy
    # BIG FILE
    # DOWNLOAD_URL = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz'
    # Small File 22MB
    DOWNLOAD_URL = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract22.xml.gz'
    data_file = 'data/enwiki-latest-abstract.xml.gz'
    if not os.path.exists(data_file):
        download_wikipedia_abstracts(data_file, DOWNLOAD_URL)


    ######################################################################################################
    # load, index and cache indexed results
    cache_file = data_file + ".cache"
    index = Index()
    if not os.path.exists(cache_file):
        index_documents(load_documents(data_file), index)
        cache.save_index(cache_file, index)
    else:
        cache.load_index(cache_file, index)
    

    ######################################################################################################
    print(f'Index contains {len(index.documents)} documents')
    results = index.search('London Beer Flood', search_type='AND')
    pprint(results)
    results = index.search('London Beer Flood', search_type='OR')
    pprint(results)
    results = index.search('London Beer Flood', search_type='AND', rank=True)
    pprint(results)
    results = index.search('London Beer Flood', search_type='OR', rank=True)
    pprint(results)
