import requests
from bs4 import BeautifulSoup

from icecream import ic


if __name__ == '__main__':
    url = 'https://tedsummaries.com'

    req = requests.get(url, 'html.parser')
    # ic(req, type(req))
    # ic(req.text)
    # ic(req.content)

    soup = BeautifulSoup(req.content, 'html.parser')
    # ic(soup)
    ret = soup.find(id='archives-2')
    # ic(ret.prettify())
    links = ret.find_all('a')
    for l in links:
        ic(l['href'])

    # with open(html_output_name, 'w') as f:
    #     f.write(req.text)
    #     f.close()



