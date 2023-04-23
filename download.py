import requests


def download_wikipedia_abstracts(data_file_path, url):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(data_file_path, 'wb') as f:
            # write every 1mb
            for i, chunk in enumerate(r.iter_content(chunk_size=1024*1024)):
                f.write(chunk)
                if i % 10 == 0:
                    print(f'Downloaded {i} megabytes', end='\r')

                    
if __name__ == '__main__':
    url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz'
    data_file = 'data/enwiki-latest-abstract.xml.gz'
    download_wikipedia_abstracts(data_file, url)
