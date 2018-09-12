from bs4 import BeautifulSoup
from .common import Common
from time import sleep, gmtime, strftime
import requests
import json


class WhatIsMyBrowser(Common):

    def __init__(self, filter='operating_system_name', value='windows', limit=500, db_enabled=True):
        self.url = 'https://developers.whatismybrowser.com/useragents/explore/{}/{}'.format(filter, value)
        self.limit = limit
        self.db_enabled = db_enabled

    def get_data(self, as_json=False):
        data = []
        page = 1

        while len(data) < self.limit:
            for item in self._read_page(page):
                if len(data) < self.limit:
                    data.append(item)
            page = page+1

        if not as_json:
            return data

        return json.dumps(data)

    def _read_page(self, page=1):
        if page > 1:
            sleep(3)

        body = requests.get('{}/{}'.format(self.url, page))

        if not bool(BeautifulSoup(body.content, "html.parser").find()):
            return []

        dataset = []
        priorities = {'Very common': 1, 'Common': 2}
        soup = BeautifulSoup(body.content, "html.parser")
        for td in soup.findAll("td", class_="useragent"):
            pop = td.parent.select_one("td:nth-of-type(5)").text
            dataset.append({
                'priority': priorities[pop],
                'agent': str(td.select_one("a").text),
                'created_at': strftime("%Y-%m-%d %H:%M:%S", gmtime())
            })

            if len(dataset) >= self.limit:
                break

        return dataset
