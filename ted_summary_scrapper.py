"""
Scrape https://tedsummaries.com and the relevant ted talks
All relevant information are in the static website
"""

import re
import json
import requests

# import bs4
from bs4 import BeautifulSoup
from icecream import ic

from util import *


def get_soup(url):
    return BeautifulSoup(requests.get(url, 'html.parser').content, 'html.parser')


def get_words(s: str) -> list[str]:
    return list(filter(bool, re.split(r'\W+', s)))  # Remove empty strings


class TedSummaryScrapper:
    def __init__(self):
        self.url = config('url_seeds.ted_summary')
        self.soup = get_soup(self.url)
        self.link_divisions = self._link_divisions_by_month()
        # ic(self.link_divisions)
        self.links = self._sum_links()
        self.links = {k: list(  # Not a summary
            filter(lambda link: link != 'https://tedsummaries.com/2014/08/03/tedsummaries-questions-to-you/', v)
        ) for k, v in self.links.items()}
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
            if not hasattr(link2dict, 'count'):
                link2dict.count = 0

            def soup2meta(s_):
                titles = s_.find_all('h1', class_='entry-title')
                assert len(titles) == 1
                title = titles[0]

                m = re.match(r'^(?P<speaker>.*?): (?P<title>.*?)$', title.text)
                return dict(
                    speaker=m.group('speaker').lower(),
                    title=m.group('title').lower()
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

                def txt2dom(s, lh=False):
                    """
                    Heuristic for the summary element
                    """
                    return (
                        (lh and '<p><span style="line-height:1.5em;"><strong>Summary</strong></span></p>') or
                        f'<p><strong>{s}</strong></p>'
                    )

                entries = s_.find_all('div', class_='entry-content')
                assert len(entries) == 1
                # The summary may contain `blockquote`s, ignored
                elms = entries[0].find_all(['p', 'ol', 'ul'])

                e_strs = [p.__str__() for p in elms]
                ic(e_strs)

                s_tho = txt2dom('My Thoughts')
                s_sum = txt2dom('Summary')
                s_sum_ = txt2dom('Summary:')
                s_sum__ = txt2dom('Summary', lh=True)
                idx_strt = (
                    (s_sum in e_strs and e_strs.index(s_sum)) or
                    (s_sum_ in e_strs and e_strs.index(s_sum_)) or
                    (s_sum__ in e_strs and e_strs.index(s_sum__))
                )
                ic(idx_strt)
                assert type(idx_strt) is int

                idx_end = (s_tho in e_strs and e_strs.index(s_tho)) or None
                elms = elms[idx_strt+1:idx_end]
                return dict(
                    summary='\n'.join(elm2str(elm) for elm in elms)
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
            print(f'Scrapping ted talk {link2dict.count+1}: [{link}]')
            soup = get_soup(link)
            d = soup2meta(soup) | soup2summary(soup)
            # if d['speaker'] == 'JANE MCGONIGAL'.lower():
            #     ic(d)
            #     exit(1)
            words = get_words(d['speaker']) + get_words(d['title'])
            # TED talk url eg: charmian_gooch_meet_global_corruption_s_hidden_players
            url_ted = f'https://www.ted.com/talks/{"_".join(words)}/transcript'
            # ic(url_ted)
            d |= soup2transcript(get_soup(url_ted))
            link2dict.count += 1
            print(f'Scrapping ted talk {link2dict.count}: [{d["title"]}] by [{d["speaker"]}] completed')
            return d

        links = flatten([
            (date, link) for link in links
        ] for date, links in self.links.items())
        for date, link in links:
            if date == (2014, 3):
                link2dict(link)
                # exit(1)
        return [dict(year=year, month=month) | link2dict(link) for (year, month), link in links]

    def export(self, fp):
        """
        Export scrapped summaries to JSON

        :param fp: File path without extension
        """
        fnm = f'{fp}.json'
        open(fnm, 'a').close()  # Create file in OS
        with open(fnm, 'w') as f:
            json.dump(self.sums, f, indent=4)


if __name__ == '__main__':
    tss = TedSummaryScrapper()
    tss.export('ted-summaries')
    # ic(tss.month_links)
