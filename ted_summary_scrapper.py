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


def get_words(s: str) -> list[str]:
    # Remove empty strings
    # return list(filter(lambda w: w, re.split(r'\W+', s)))
    return list(filter(bool, re.split(r'\W+', s)))


class TedSummaryScrapper:
    def __init__(self):
        self.url = config('url_seeds.ted_summary')
        self.soup = get_soup(self.url)
        self.link_divisions = self._link_divisions_by_month()
        ic(self.link_divisions)
        self.links = self._sum_links()
        ic(self.links, len(flatten(self.links.values())))
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
            def soup2summary(soup):
                """
                :param soup: `BeautifulSoup` object for a `tedsummaries` page
                """
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
                elms = elms[idx_strt+1 : idx_end]
                # ic(elms)
                return dict(
                    summary='\n'.join(elm2str(elm) for elm in elms)
                )

            def soup2meta(soup):
                titles = soup.find_all('h1', class_='entry-title')
                assert len(titles) == 1
                title = titles[0]

                m = re.match(r'^(?P<speaker>.*?): (?P<title>.*?)$', title.text)
                return dict(
                    speaker=m.group('speaker').lower(),
                    title=m.group('title').lower()
                )

            def soup2transcript(soup: BeautifulSoup):
                """
                :param soup: `BeautifulSoup` object for a `ted` talk page
                """
                # ic(soup.prettify())
                # trans_clusters = soup.find_all('div', class_=['Grid', 'Grid--with-gutter'])
                trans_clusters = soup.select('div.Grid.Grid--with-gutter')

                def cluster2txt(cls):
                    # ic(cls, type(cls))
                    ps = cls.find_all('p')
                    # ic(ps)
                    assert len(ps) == 1
                    p = ps[0]

                    ic(p.text)
                    print(p.text)
                    # txt = p.text.replace('\t', '')
                    txt = re.sub(r'[\t]+', '', p.text)
                    txt = re.sub(r'[\n]+', ' ', txt)
                    # ic(txt)
                    # print(txt)
                    return txt
                    # exit(1)
                # ic(trans_clusters)
                # ic(len(trans_clusters))
                # ic(cluster2txt(trans_clusters[0]))
                return dict(
                    transcript='\n'.join(cluster2txt(cls) for cls in trans_clusters)
                )
            soup = get_soup(link)
            d = soup2summary(soup) | soup2meta(soup)
            ic(d)
            # url = d['title']
            words = get_words(d['speaker']) + get_words(d['title'])
            # ic(words)
            # TED talk url eg: charmian_gooch_meet_global_corruption_s_hidden_players
            url_ted = f'https://www.ted.com/talks/{"_".join(words)}/transcript'
            ic(url_ted)
            return d | soup2transcript(get_soup(url_ted))
            # return [link2dict(link) for link in links]

        links = flatten([
            (date, link) for link in links
        ] for date, links in self.links.items())
        return [dict(year=year, month=month) | link2dict(link) for (year, month), link in links]


if __name__ == '__main__':
    tss = TedSummaryScrapper()
    # ic(tss.month_links)
