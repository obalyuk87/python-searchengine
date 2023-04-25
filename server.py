#!/bin/python3

import os.path
from download import download_wikipedia_abstracts
from load import load_documents
from search.timing import timing
from search.index import Index
import cache
import time
from flask import Flask, render_template, request

# BIG FILE
# DOWNLOAD_URL = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz'
# Small File 22MB
DOWNLOAD_URL = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract22.xml.gz'
DATA_FILE_PATH = 'data/enwiki-latest-abstract.xml.gz'

@timing
def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'- indexed {i} documents', end='\r')
    return index

def create_app():
    print("- creating Application")
    global index

    # Load Index
    cache_file = DATA_FILE_PATH + ".cache"
    if not os.path.exists(cache_file):
        # Download File 
        if not os.path.exists(DATA_FILE_PATH):
            download_wikipedia_abstracts(DATA_FILE_PATH, DOWNLOAD_URL)
            print(f'- loaded File to {DATA_FILE_PATH} from {DOWNLOAD_URL}')

        index_documents(load_documents(DATA_FILE_PATH), index)
        cache.save_index(cache_file, index)
    else:
        cache.load_index(cache_file, index)
    
    # Start Web-App
    app = Flask(__name__)
    return app

###############################################################################
# Initialize Application
index = Index()
app = create_app()
###############################################################################

@app.route("/show-dataset")
def hello_world():
    global index
    print(f'- index contains {len(index.documents)} documents')
    return index.show_documents(1000)

@app.route("/")
def home():
    global index
    tplVars = {}

    args = request.args
    params = args.to_dict()
    search = params.get("search") 
    type = params.get("search_type")
    ranked = params.get("ranked") == "yes"
    # add the input params back into the form
    for key,value in params.items():
        tplVars[key] = value

    # 
    query = f'Search="{search}" Type="{type}" Ranked="{ranked}"'
    tplVars['query'] = query
    tplVars['results'] = None
    tplVars['results_count'] = None
    tplVars['dataset_count'] = len(index.documents)
    tplVars['dataset_url'] = DOWNLOAD_URL
    if search:
        print("- running search " + query)
        start = time.time()
        results = index.search(search, type, ranked)
        end = time.time()
        
        tplVars['results'] = results
        tplVars['results_count'] = len(results)
        tplVars['search_duration'] = round((end - start) * 100, 4)

    return render_template('index.html', vars=tplVars)


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)