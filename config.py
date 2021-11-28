from icecream import ic


config = dict(
    url_seeds=dict(
        ted='https://www.ted.com/talks',
        ted_summary='https://tedsummaries.com'
    ),
    heuristics=dict(
        url_ignore=[
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
        ],
        meta_map={  # From titles in tedsummaries.com to the metadata on ted.com
            # Some earlier entries that doesn't follow the heuristic; Or the ted.com title updated
            'Will Marshall: Tiny satellites that photograph the entire planet, every day': dict(
                speaker='Will Marshall',
                title='Tiny satellites show us the Earth as it changes in near-real-time'
            ),
            'Nicholas Stern: The state of the climate - and what we might do about it': dict(
                speaker='Lord Nicholas Stern', title='The state of the climate - and what we might do about it'
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
            'Arthur Benjamin: Lightning calculation and other "Mathemagic"': dict(
                speaker='Arthur Benjamin', title='A performance of "Mathemagic"'
            ),
            'Hans Rosling: Debunking third-world myths with the best stats you\'ve ever seen': dict(
                speaker='Hans Rosling', title='The best stats you\'ve ever seen'
            ),
            'Ed Yong: Suicidal wasps, zombie roaches and other parasite tales': dict(
                speaker='Ed Yong', title='Zombie roaches and other parasite tales'
            ),
            'Pattie Maes (and Pranav Mistry): Unveiling game-changing wearable tech': dict(
                speaker='Pattie Maes + Pranav Mistry', title='Meet the SixthSense interaction'
            ),
            'Jamie Oliver\'s TED Prize wish: Teach every child about food': dict(
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
            'Jill Bolte Taylor\'s stroke of insight': dict(
                speaker='Jill Bolte Taylor', title='My stroke of insight'
            ),
            'A realistic vision for World Peace': dict(
                speaker='Jody Williams', title='A realistic vision for World Peace'
            ),
            'Treating violence as a contagious disease': dict(
                speaker='Gary Slutkin', title='Let\'s treat violence like a contagious disease'
            ),
            'Online Filter Bubbles': dict(
                speaker='Eli Pariser', title='Beware online "Filter Bubbles"'
            ),
            'Can technology solve big problems?': dict(
                speaker='Jason Pontin', title='Can technology solve our big problems?'
            )
        }
    )
)

if __name__ == "__main__":
    import json

    fl_nm = 'config.json'
    ic(config)
    with open(fl_nm, 'w') as f:
        json.dump(config, f, indent=4)
