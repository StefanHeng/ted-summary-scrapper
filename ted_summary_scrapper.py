"""
Scrape https://tedsummaries.com and the relevant ted talks
All relevant information are in the static website
"""

import re
import requests

import bs4
from bs4 import BeautifulSoup
from icecream import ic

from util import *


def get_soup(url):
    return BeautifulSoup(requests.get(url, 'html.parser').content, 'html.parser')


class TedSummaryScrapper:
    def __init__(self):
        self.url = config('url_seeds.ted_summary')
        ic(self.url)
        self.soup = get_soup(self.url)
        self.month_links = self._month_links()
        ic(self.month_links)
        self.links = self._sum_links()

    def _month_links(self):
        links = [link['href'] for link in self.soup.find(id='archives-2').find_all('a')]
        ms = [(re.match(r'.*?(?P<year>\d{4})[/](?P<month>\d{2})[/]$', link), link) for link in links]
        # for m, _ in ms:
        #     ic(m.group('year'), m.group('month'))
        # ic(ms[0][0].group('year'))
        return {
            (m.group('year'), m.group('month')): link for m, link in ms
        }
        # return {l.text: l['href'] for l in links}

    def _sum_links(self):
        for month, link in self.month_links.items():
            ic(link)
            soup = get_soup(link)
            entries = soup.find_all('div', class_='entry-content')
            for e in entries:
                ps = e.find_all('p')
                # ic(ps[:3])
                idx_strt = [p.__str__() for p in ps].index('<p><strong>Summary</strong></p>')
                idx_end = [p.__str__() for p in ps].index('<p><strong>My Thoughts</strong></p>')
                ic(idx_strt, ps[idx_strt])
                ps = ps[idx_strt+1:idx_end]
                ic(ps)
                # for p in ps:
                #
                #     p: bs4.element.Tag
                #     ic(type(p))
                #     s = p.__str__()
                #     ic(p, s)
                    # ic(p.prettify())
                # ic(entry)
            exit(1)


if __name__ == '__main__':
    tss = TedSummaryScrapper()
    # ic(tss.month_links)
