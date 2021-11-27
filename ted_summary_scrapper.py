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
        self.fp = fp

        self.soup = get_soup(self.url)
        self.link_divisions = self._link_divisions_by_month()
        self.links = self._sum_links()
        # TODO: config()
        LINK_IGNORE = [
                # Not a summary
                'https://tedsummaries.com/2014/08/03/tedsummaries-questions-to-you/',
                'https://tedsummaries.com/2013/10/05/welcome/',
                # Not found on ted.com
                'https://tedsummaries.com/2013/12/27/the-paradoxes-of-power-in-australia-geoff-aigner/',
                'https://tedsummaries.com/2013/10/06/biochemical-degradation-of-plastics-phthalates/',
                'https://tedsummaries.com/2015/03/04/barbara-oakley-learning-how-to-learn/',
                'https://tedsummaries.com/2015/01/19/heather-white-its-not-about-working-the-room/',
                'https://tedsummaries.com/2014/04/17/the-most-important-lesson-from-83000-brain-scans-daniel-amen/',
                'https://tedsummaries.com/2014/04/14/think-small-alastair-humphreys/',
                'https://tedsummaries.com/2014/02/18/the-new-way-to-work-charlie-hoehn/',
                'https://tedsummaries.com/2014/02/13/the-discipline-of-finishing-conor-neill/',
                'https://tedsummaries.com/2013/10/05/how-to-learn-anything-in-20-hours/',
                # Found on ted.com without transcripts
                'https://tedsummaries.com/2015/03/24/ymir-vigfusson-why-i-teach-people-how-to-hack/'
            ]
        self.links = {k: list(filter(lambda link: link not in LINK_IGNORE, v)) for k, v in self.links.items()}
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
                txt = str(titles[0].text)
                txt = txt.replace('\xa0', ' ')
                ic(txt)

                m = re.match(r'^(?P<speaker>.*?): (?P<title>.*?)$', txt)
                d_map = {  # Some earlier entries that doesn't follow the heuristic; Or the ted.com title updated
                    'Will Marshall: Tiny satellites that photograph the entire planet, every day': dict(
                        speaker='Will Marshall',
                        title='Tiny satellites show us the Earth as it changes in near-real-time'
                    ),
                    'Nicholas Stern: The state of the climate — and what we might do about it': dict(
                        speaker='Lord Nicholas Stern', title='The state of the climate — and what we might do about it'
                    ),
                    'Hans Rosling and Osa Rosling: How not to be ignorant about the world': dict(
                        speaker='Hans and Ola Rosling', title='How not to be ignorant about the world'
                    ),
                    'Johnny Lee: Wii Remote hacks': dict(
                        speaker='Johnny Lee', title='Free or Cheap Wii Remote hacks'
                    ),
                    'My philosophy for a happy life: Sam Berns': dict(
                        speaker='Sam Berns', title='My philosophy for a happy life'
                    ),
                    'Arthur Benjamin: Lightning calculation and other “Mathemagic”': dict(
                        speaker='Arthur Benjamin', title='A performance of “Mathemagic”'
                    ),
                    'Hans Rosling: Debunking third-world myths with the best stats you’ve ever seen': dict(
                        speaker='Hans Rosling', title='The best stats you’ve ever seen'
                    ),
                    'Ed Yong: Suicidal wasps, zombie roaches and other parasite tales': dict(
                        speaker='Ed Yong', title='Zombie roaches and other parasite tales'
                    ),
                    'Pattie Maes (and Pranav Mistry): Unveiling game-changing wearable tech': dict(
                        speaker='Pattie Maes + Pranav Mistry', title='Meet the SixthSense interaction'
                    ),
                    'Jamie Oliver’s TED Prize wish: Teach every child about food': dict(
                        speaker='Jamie Oliver', title='Teach every child about food'
                    ),
                    'Rory Sutherland: Life lessons of an Ad Man': dict(
                        speaker='Rory Sutherland', title='Life lessons from an ad Man'
                    ),
                    'James Randi: Homeopathy, Psychics and fraud': dict(
                        speaker='James Randi', title='Homeopathy, quackery and fraud'
                    ),
                    'Kary Mullis: Celebrating the scientific experiment': dict(
                        speaker='Kary Mullis', title='Play! Experiment! Discover!'
                    ),
                    'Jill Bolte Taylor’s stroke of insight': dict(
                        speaker='Jill Bolte Taylor', title='My stroke of insight'
                    ),
                    'A realistic vision for World Peace': dict(
                        speaker='Jody Williams', title='A realistic vision for World Peace'
                    ),
                    'Treating violence as a contagious disease': dict(
                        speaker='Gary Slutkin', title='Let\'s treat violence like a contagious disease'
                    ),
                    'Online Filter Bubbles': dict(
                        speaker='Eli Pariser', title='Beware online “Filter Bubbles”'
                    ),
                    'Can technology solve big problems?': dict(
                        speaker='Jason Pontin', title='Can technology solve our big problems?'
                    )
                }
                return (  # Noise in the blog
                    (txt in d_map and d_map[txt]) or
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

            def ted_url2transcript(url, patience=5):
                """
                :param url: URL for a `ted` talk page
                :param patience: Sometimes requesting the webpage results in the webpage not expected
                """

                s_ = get_soup(url)
                title = s_.find('title').string
                # ic(s_.find('title').string)
                req_lim_err = '429 Rate Limited too many requests'
                unexpected_err = 'TED: Ideas Worth Spreading'  # Not sure why
                while req_lim_err in title or unexpected_err in title:
                    if req_lim_err in title:
                        warn('Encountered ted.com request limit error, sleeping')
                    else:
                        ic(s_.prettify())
                        warn('Encountered ted.com unexpected response error, sleeping')
                    sleep(2)
                    s_ = get_soup(url)
                    title = s_.find('title').string
                # ic(s_.prettify())
                trans_clusters = s_.select('div.Grid.Grid--with-gutter')
                # if link == 'https://tedsummaries.com/2014/12/06/sheena-iyengar-how-to-make-choosing-easier/':
                #     ic(s_.prettify())
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
            ic(url_ted)
            d |= ted_url2transcript(url_ted)
            d |= dict(url_summary=link, url_ted=url_ted)
            d |= dict(url_summary=link, url_ted=url_ted)

            # if link == 'https://tedsummaries.com/2014/12/22/jeremy-howard-the-wonderful-and-terrifying-implications-of-computers-that-can-learn/':
            #     ic(d['transcript'])
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
    # export()

    def sanity_check():
        with open('ted-summaries.json', 'r') as f:
            lst = json.load(f)
            # ic(len(lst), lst[:5])
            count = 0
            for d in lst:
                if len(d['transcript']) == 0:
                    ic(d['title'], d['url_summary'], d['url_ted'])
                    count += 1
            ic(count)
    sanity_check()

