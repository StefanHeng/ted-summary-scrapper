"""
Scrape https://tedsummaries.com and the relevant ted talks
All relevant information are in the static website
"""

import re
from typing import Union
from warnings import warn
import json
import requests
from time import sleep

from bs4 import BeautifulSoup
from icecream import ic

from util import *


def get_soup(url):
    return BeautifulSoup(requests.get(url, 'html.parser').content, 'html.parser')


def get_words(s: str) -> list[str]:
    return list(filter(bool, re.split(r'\W+', s)))  # Remove empty strings


# def clean_text(s: str):
#     # How can I remove those Unicode characters?
#     s = s.replace('\xa0', ' ')
#     s = s.replace('\u2019', "'")


class TedSummaryScrapper:
    def __init__(self, fp='ted-summaries'):
        """
        Scrapped summaries are written to JSON file

        :param fp: File path without extension
        """
        self.url = config('url_seeds.ted_summary')
        self.url_ted = config('url_seeds.ted')
        self.meta_map = config('heuristics.meta_map')
        self.url_ignore = config('heuristics.url_ignore')
        self.fp = fp

        self.soup = get_soup(self.url)
        self.link_divisions = self._link_divisions_by_month()
        self.links = self._sum_links()
        self.links = {k: list(filter(
            lambda link: link not in self.url_ignore, v)
        ) for k, v in self.links.items()}
        print(f'Scraping {len(flatten(self.links.values()))} talks... ')
        # ic(self.links)
        self.sums = self._sums()
        # ic(self.sums)
        self.export()

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
        def link2dict(link):
            if not hasattr(link2dict, 'count'):
                link2dict.count = 0

            def soup2meta(s_):
                titles = s_.find_all('h1', class_='entry-title')
                assert len(titles) == 1
                title = str(titles[0].text)
                title = title.replace('\xa0', ' ')

                m = re.match(r'^(?P<speaker>.*?): (?P<title>.*?)$', title)
                return (  # Noise in the blog
                    (title in self.meta_map and self.meta_map[title]) or
                    dict(speaker=m.group('speaker'), title=m.group('title'))
                )

            def soup2summary(s_):
                """
                :param s_: `BeautifulSoup` object for a `tedsummaries` page
                """
                def elm2str(elm):
                    if elm.name == 'p':
                        return elm.text
                    else:  # `ol` or 'ul'
                        return '\n'.join(f'{idx+1}. {li.text}' for idx, li in enumerate(elm.find_all('li')))

                def contains_text(elm, txt: Union[str, list[str]]):
                    texts_elm = [s.text for s in elm.find_all('strong')]
                    if not isinstance(txt, list):
                        txt = [txt]
                    return any(t in texts_elm for t in txt)

                entries = s_.find_all('div', class_='entry-content')
                assert len(entries) == 1
                # The summary may contain `blockquote`s, ignored
                elms = entries[0].find_all(['p', 'ol', 'ul'])
                # There should always be one
                elm_sums = list(filter(lambda e: contains_text(e, ['Summary', 'Summary:']), elms))
                assert len(elm_sums) == 1
                idx_strt = elms.index(elm_sums[0])
                assert type(idx_strt) is int

                elm_2nd = list(filter(lambda e: contains_text(e, ['My Thoughts', 'Critique']), elms))
                if elm_2nd:
                    idx_end = elms.index(elm_2nd[0])
                else:
                    idx_end = None
                    warn(f'Title after summary not found for [{link}]')
                elms = elms[idx_strt+1:idx_end]
                return dict(
                    summary='\n'.join(elm2str(elm) for elm in elms)
                )

            def ted_url2transcript(url):
                """
                :param url: URL for a `ted` talk page
                """
                s_ = get_soup(url)
                title = s_.find('title').string
                req_lim_err = '429 Rate Limited too many requests'
                unexpected_err = 'TED: Ideas Worth Spreading'  # Not sure why
                while req_lim_err in title or unexpected_err in title:
                    if req_lim_err in title:
                        warn('Encountered ted.com request limit error, sleeping')
                    else:
                        warn('Encountered ted.com unexpected response error, sleeping')
                    sleep(2)
                    s_ = get_soup(url)
                    title = s_.find('title').string
                trans_clusters = s_.select('div.Grid.Grid--with-gutter')
                if len(trans_clusters) == 0:
                    ic(s_.prettify())
                assert len(trans_clusters) >= 1

                def cluster2txt(cls):
                    ps = cls.find_all('p')
                    assert len(ps) == 1
                    txt = re.sub(r'[\t]+', '', ps[0].text)
                    return re.sub(r'[\n]+', ' ', txt)
                return dict(
                    transcript='\n'.join(cluster2txt(cls) for cls in trans_clusters)
                )
            print(f'Scrapping TED talk {link2dict.count+1}: [{link}]')
            soup = get_soup(link)
            d = soup2meta(soup) | soup2summary(soup)
            words = get_words(d['speaker'].lower()) + get_words(d['title'].lower())
            # TED talk url eg: charmian_gooch_meet_global_corruption_s_hidden_players
            url_ted = f'{self.url_ted}/{"_".join(words)}/transcript'
            d |= ted_url2transcript(url_ted)
            d |= dict(url_summary=link, url_ted=url_ted)
            d |= dict(url_summary=link, url_ted=url_ted)

            link2dict.count += 1
            print(f'Completed scrapping TED talk {link2dict.count}: [{d["title"]}] by [{d["speaker"]}]')
            return d

        links = flatten([
            (date, link) for link in links
        ] for date, links in self.links.items())
        # for date, link in links:
        #     if date == (2013, 10):
        #         link2dict(link)
        return [dict(year=year, month=month) | link2dict(link) for (year, month), link in links]

    def export(self):
        fnm = f'{self.fp}.json'
        open(fnm, 'a').close()  # Create file in OS
        with open(fnm, 'w') as f:
            json.dump(self.sums, f, indent=4)
            print(f'Scrapping & file write complete at [{fnm}]')


if __name__ == '__main__':
    def export():
        tss = TedSummaryScrapper()
    export()

    def sanity_check():
        with open('ted-summaries.json', 'r') as f:
            lst = json.load(f)
            for d in lst:
                assert len(d['transcript']) >= 1
    sanity_check()

