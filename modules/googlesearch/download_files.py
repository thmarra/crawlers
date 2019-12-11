import requests
from bs4 import BeautifulSoup
import sys
import re
import os
import urllib
import uuid


def parse_file_url(query):
    parsed = urllib.parse.urlparse(query)
    pieces = urllib.parse.parse_qs(parsed.query)
    if 'q' in pieces:
        return pieces['q'][0]
    return None


def parse_filename(url):
    parsed = urllib.parse.urlparse(url)
    name = parsed.path.rsplit('/', 1)[1]
    if not len(name):
        name = str(uuid.uuid4())
    if not name.endswith('.pdf'):
        name = name + '.pdf'
    return name


def walk_page(response, download_path, i, limit):
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find('div', {'id': 'main'}).find_all('div', {'class': 'kCrYT'})

    for div in divs:
        if i > limit:
            return i

        link = div.find('a', href=True)

        if link is None:
            continue

        url = parse_file_url(link['href'])

        filename = parse_filename(url)
        filename = os.path.join(download_path, filename)

        print('Looking for file {}'.format(i), url, sep="\n")

        try:
            file = requests.get(url)
            if file.status_code is 200 \
                and file.headers['content-type'] == 'application/pdf' \
                and int(file.headers['content-length']) > 0:
                print('Saving file {}'.format(i))
                with open(filename, 'wb') as f:
                    f.write(file.content)
                i = i+1
        except Exception as e:
            print("Could not download file", e)

    return i


def search(query, download_path, filetype='pdf', language='pt-BR', as_qdr='all', count=15):
    if not os.path.exists(download_path):
        print("Download dir not found")
        sys.exit()

    i = 1
    p = 6
    s = requests.Session()

    while count > i:
        params = urllib.parse.urlencode({
            'hl': language,
            'as_qdr': as_qdr,
            'q': '{} filetype:{}'.format(query, filetype),
            'start': (p - 1) * 10
        })
        url = 'https://www.google.com/search?{}'.format(params)

        print("Searching page {} - file number {}".format(p, i), url, sep="\n")

        response = s.get(url, timeout=10)
        i = walk_page(i=i, limit=count, response=response,
                      download_path=download_path)
        print('Done', i)
        p = p + 1


filepath = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(filepath, '..', '..', 'sample_pdf')
search(query='pdf', download_path=filepath)
