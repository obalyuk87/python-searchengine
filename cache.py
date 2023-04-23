import pickle
import time
from search.index import Index

def save_index(filepath: str, index: Index):
    start = time.time()
    payload = {"idx": index.index, "docs": index.documents }
    with open(filepath, "wb") as outfile:
        pickle.dump(payload, outfile)
    end = time.time()
    print(f'save_index took {end - start} seconds')


def load_index(filepath: str, index: Index):
    start = time.time()
    with open(filepath, "rb") as infile:
        cache = pickle.load(infile)
        index.index = cache["idx"]
        index.documents = cache["docs"]
    end = time.time()
    print(f'load_index took {end - start} seconds')
