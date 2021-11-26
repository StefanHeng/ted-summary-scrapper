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


def get_words(s: str) -> list[str]:
    # Remove empty strings
    return list(filter(bool, re.split(r'\W+', s)))


class TedSummaryScrapper:
    def __init__(self):
        self.url = config('url_seeds.ted_summary')
        self.soup = get_soup(self.url)
        self.link_divisions = self._link_divisions_by_month()
        # ic(self.link_divisions)
        self.links = self._sum_links()
        # ic(self.links, len(flatten(self.links.values())))
        self.sums = self._sums()
        ic(self.sums)

    def _link_divisions_by_month(self):
        links = [link['href'] for link in self.soup.find(id='archives-2').find_all('a')]
        ms = [(re.match(r'.*?(?P<year>\d{4})[/](?P<month>\d{2})[/]$', link), link) for link in links]
        return {
            (int(m.group('year')), int(m.group('month'))): link for m, link in ms
        }

    def _sum_links(self):
        def _links(link_date):
            soup = get_soup(link_date)
            entries = soup.find_all('h1', class_='entry-title')

            def _link(entry):
                links = entry.find_all('a')
                assert len(links) == 1
                return links[0]['href']
            return [_link(e) for e in entries]
        return {date: _links(link) for date, link in self.link_divisions.items()}

    def _sums(self) -> list[dict]:
        """
        :return: List of ted summary objects, containing the date, speaker, title, talk transcript and summary
        """
        # for month, links in self.links.items():
        def link2dict(link):
            # if month == (2015, 4):
            #     ic(link)
            def soup2summary(s_):
                """
                :param s_: `BeautifulSoup` object for a `tedsummaries` page
                """
                entries = s_.find_all('div', class_='entry-content')
                assert len(entries) == 1
                entry = entries[0]

                def elm2str(elm):
                    if elm.name == 'p':
                        return elm.text
                    else:  # `ol` or 'ul'
                        ic('here')
                        return '\n'.join(f'{idx+1}. {li.text}' for idx, li in enumerate(elm.find_all('li')))

                elms = entry.find_all(['p', 'ol', 'ul'])
                idx_strt = [p.__str__() for p in elms].index('<p><strong>Summary</strong></p>')
                idx_end = [p.__str__() for p in elms].index('<p><strong>My Thoughts</strong></p>')
                elms = elms[idx_strt+1:idx_end]
                return dict(
                    summary='\n'.join(elm2str(elm) for elm in elms)
                )

            def soup2meta(s_):
                titles = s_.find_all('h1', class_='entry-title')
                assert len(titles) == 1
                title = titles[0]

                m = re.match(r'^(?P<speaker>.*?): (?P<title>.*?)$', title.text)
                return dict(
                    speaker=m.group('speaker').lower(),
                    title=m.group('title').lower()
                )

            def soup2transcript(s_: BeautifulSoup):
                """
                :param s_: `BeautifulSoup` object for a `ted` talk page
                """
                trans_clusters = s_.select('div.Grid.Grid--with-gutter')

                def cluster2txt(cls):
                    ps = cls.find_all('p')
                    assert len(ps) == 1
                    txt = re.sub(r'[\t]+', '', ps[0].text)
                    return re.sub(r'[\n]+', ' ', txt)
                return dict(
                    transcript='\n'.join(cluster2txt(cls) for cls in trans_clusters)
                )
            soup = get_soup(link)
            d = soup2summary(soup) | soup2meta(soup)
            words = get_words(d['speaker']) + get_words(d['title'])
            # TED talk url eg: charmian_gooch_meet_global_corruption_s_hidden_players
            url_ted = f'https://www.ted.com/talks/{"_".join(words)}/transcript'
            # ic(url_ted)
            return d | soup2transcript(get_soup(url_ted))

        links = flatten([
            (date, link) for link in links
        ] for date, links in self.links.items())
        for date, link in links:
            if date == (2015, 4):
                ic(link2dict(link))
                exit(1)
        # return [dict(year=year, month=month) | link2dict(link) for (year, month), link in links]


if __name__ == '__main__':
    tss = TedSummaryScrapper()
    # ic(tss.month_links)
