import requests
from bs4 import BeautifulSoup

from icecream import ic


# def make_soup(url):
#     try:
#         html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}).content
#     except:
#         return None
#     return BeautifulSoup(html, "lxml")


if __name__ == '__main__':
    # url = "http://www.alibaba.com/Agricultural-Growing-Media_pid144"
    # soup = make_soup(url)
    #
    # print(soup.select_one("a.next").get('href'))
    # url = input('Webpage to grab source from: ')
    # html_output_name = input('Name for html file: ')
    url = 'https://tedsummaries.com'

    req = requests.get(url, 'html.parser')
    # ic(req, type(req))
    # ic(req.text)
    # ic(req.content)

    soup = BeautifulSoup(req.content, "html.parser")
    # ic(soup)
    ret = soup.find(id='archives-2')
    # ic(ret.prettify())
    links = ret.find_all('a')
    for l in links:
        ic(l['href'])

    # with open(html_output_name, 'w') as f:
    #     f.write(req.text)
    #     f.close()



