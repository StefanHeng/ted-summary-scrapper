from icecream import ic


if __name__ == '__main__':
    import re

    m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
    ic(m.groups())

    s = 'https://tedsummaries.com/2014/04/'
    ic(s)
    m = re.match(r".*?(\d+)", '2014/04/')
    ic(m.groups())
    m = re.match(r'.*?(?P<year>\d{4})[/](?P<month>\d{2})[/]$', 'https://tedsummaries.com/2014/04/')
    ic(m and m.groups())
    ic(m.group('year'))
    ic(m.group('month'))

    # ic(re.match(r'(\d{4})', s))
    # ic(re.match(r'^/\d{4}/\d{2}/$', s))

    ic(re.split(r'\W+', 'Words, words, words.'))

    myString = "I want to Remove all white \t spaces, new lines \n and tabs \t"
    ic(re.sub(r"[\n\t\s]*", "", myString))
    ic(re.sub(r"[\n\t]+", "", myString))

