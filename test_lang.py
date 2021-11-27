from icecream import ic


if __name__ == '__main__':
    # import re
    #
    # m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
    # ic(m.groups())
    #
    # s = 'https://tedsummaries.com/2014/04/'
    # ic(s)
    # m = re.match(r".*?(\d+)", '2014/04/')
    # ic(m.groups())
    # m = re.match(r'.*?(?P<year>\d{4})[/](?P<month>\d{2})[/]$', 'https://tedsummaries.com/2014/04/')
    # ic(m and m.groups())
    # ic(m.group('year'))
    # ic(m.group('month'))
    #
    # # ic(re.match(r'(\d{4})', s))
    # # ic(re.match(r'^/\d{4}/\d{2}/$', s))
    #
    # ic(re.split(r'\W+', 'Words, words, words.'))
    #
    # myString = "I want to Remove all white \t spaces, new lines \n and tabs \t"
    # ic(re.sub(r"[\n\t\s]*", "", myString))
    # ic(re.sub(r"[\n\t]+", "", myString))

    # arr = [1, 2, 3]
    # ic(arr.index(4))

    s = 'Meet global corruption\u2019s hidden players'
    s2 = "Ken Jennings loved game shows from a young age, and felt extreme satisfaction when he beat his parents at " \
         "Trivial Pursuit \u201cKnowledge is Power\u201d. In 2004 he appeared on Jeopardy for the first time, " \
         "but in 2009 he got a call from the producers\u00a0asking him to play against IBM\u2019s Jeopardy machine: " \
         "Watson. Because of his love of the game he agreed, but also because he knew about AI at the time and " \
         "thought he could win. It is\u00a0extremely difficult for computers to understand language and the nuance of " \
         "natural communication, so Ken was confident. As the time came closer, he saw\u00a0graphs of Watson\u2019s " \
         "performance against other Jeopardy players\u2019 skill level, slowly creeping towards his own. He knew the " \
         "AI was coming for him \u2013 not in the gunsights of Terminator, but in a line of data slowly creeping " \
         "upwards.\nOn the day IBM programmers came out to support Watson, and Watson won handily. He remembers " \
         "feeling the same way a Detroit factory worker did \u2013 realising his job had been made obsolete by a " \
         "robot. He was one of the first, but not only knowledge worker to have this feeling: pharmacists, " \
         "paralegals, sports journalists are also slowly being overtaken by thinking machines. In a lot of cases, " \
         "the machines don\u2019t show the same creativity, but they do the job much more cheaply and quickly than a " \
         "human.\nAs computers take over thinking jobs, do humans still need to learn anything, " \
         "or know anything?\u00a0Will our brains shrink as more tasks get outsourced, and computers remember more " \
         "facts?\nKen believes having this knowledge in your head is still important because of volume and time.\n1. " \
         "Volume because the amount of information is doubling every 18 months, and we need to make good judgements " \
         "on these facts. We need the facts in our head to assemble a decision, it is harder to judge these facts " \
         "while looking them up.\n2. Time because sometimes you need a quick decision, or need to know what to do. " \
         "Ken talks about a child remembering a fact from Geography at the beach: the tide rushing out is a precursor " \
         "to a Tsunami. Her knowledge and quick response on the day of the 2004 boxing day tsunami saved the people " \
         "on that beach, which couldn\u2019t be done unless she knew it.\nShared knowledge is also an important " \
         "social glue: people can bond over a shared experience or knowing something in a way that can\u2019t be " \
         "simulated by looking things up together.\nKen doesn\u2019t want to live in a world where knowledge is " \
         "obsolete, or where humanity has no shared cultural knowledge. Right now, we need to make the decision " \
         "of\u00a0what our future will be like: will we go to an information golden age where we use our extra access " \
         "to knowledge, or will we not bother to learn anymore? Ken wants us to keep being curious, inquisitive " \
         "people \u2013 to have an unquenchable curiosity. "
    print(s, s2)
    ic(s, str(s))
    ic(s.encode('ascii', 'ignore'))
    ic(s.encode('utf-8', 'ignore'))
    ic(s2.encode('ascii', 'ignore'))
    ic(s2.encode('utf-8', 'ignore'))

    import requests
    res = requests.get('https://tedsummaries.com', 'html.parser')
    ic(res.encoding)


