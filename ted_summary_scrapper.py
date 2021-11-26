"""
Scrape https://tedsummaries.com and the relevant ted talks
All relevant information are in the static website
"""

import re

import ent as ent
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
        # ic(self.url)
        self.soup = get_soup(self.url)
        self.month_links = self._month_links()
        # ic(self.month_links)
        self.links = self._sum_links()
        # ic(self.links, len(flatten(self.links.values())))
        self.sums = self._sum()

    def _month_links(self):
        links = [link['href'] for link in self.soup.find(id='archives-2').find_all('a')]
        ms = [(re.match(r'.*?(?P<year>\d{4})[/](?P<month>\d{2})[/]$', link), link) for link in links]
        return {
            (int(m.group('year')), int(m.group('month'))): link for m, link in ms
        }

    def _sum_links(self):
        def _links(link_month):
            soup = get_soup(link_month)
            entries = soup.find_all('h1', class_='entry-title')

            def _link(entry):
                links = entry.find_all('a')
                assert len(links) == 1
                return links[0]['href']
            return [_link(e) for e in entries]
            # if month == (2015, 4):
            #     ic(link)
        return {month: _links(link) for month, link in self.month_links.items()}

    def _sum(self):
        for month, links in self.links.items():
            def soup2summary(soup):
                entries = soup.find_all('div', class_='entry-content')
                assert len(entries) == 1
                entry = entries[0]

                def elm2str(elm):
                    if elm.name == 'p':
                        return elm.text
                    else:  # `ol`
                        ic('here')
                        return '\n'.join(li.text for li in elm.find_all('li'))

                elms = entry.find_all(['p', 'ol'])
                # ic(elms)
                idx_strt = [p.__str__() for p in elms].index('<p><strong>Summary</strong></p>')
                idx_end = [p.__str__() for p in elms].index('<p><strong>My Thoughts</strong></p>')
                elms = elms[idx_strt + 1:idx_end]
                # ic(elms)
                return '\n'.join(elm2str(elm) for elm in elms)

            def soup2meta(soup):
                titles = soup.find_all('h1', class_='entry-title')
                assert len(titles) == 1
                title = titles[0]

                m = re.match(r'^(?P<speaker>.*?):(?P<title>.*?)$', title.text)
                ic(m.group('speaker'), m.group('title'))

            def soup2dict(soup):
                ic(soup2summary(soup))
                soup2meta(soup)
                ic('here')
                exit(1)

            # exit(1)
            return [soup2dict(get_soup(link)) for link in links]


if __name__ == '__main__':
    tss = TedSummaryScrapper()
    # ic(tss.month_links)
