from functools import reduce
from typing import TypeVar, Generic, Iterable
import json
import re
import unicodedata


T = TypeVar('T')


def get(dic, ks):
    """
    :param dic: Potentially multi-level dictionary
    :param ks: Potentially `.`-separated keys
    """
    ks = ks.split('.')
    return reduce(lambda acc, elm: acc[elm], ks, dic)


def config(attr):
    """
    Retrieves the queried attribute value from the config file.

    Loads the config file on first call.
    """
    if not hasattr(config, 'config'):
        # with open(f'{PATH_BASE}/{DIR_PROJ}/config.json') as f:
        with open('config.json') as f:
            config.config = json.load(f)
    return get(config.config, attr)


def flatten(lst):
    """
    Flatten list of list into
    """
    return sum(lst, [])


def get_words(s: str) -> list[str]:
    return list(filter(bool, re.split(r'\W+', s)))  # Remove empty strings


def strip_accents(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')


def unicode2ascii(s: str):
    # s = re.sub('\xa0|\u00a0', ' ', s)
    s = re.sub('[\u00a0]', ' ', s)
    # s = s.replace('\u2013', '-')
    s = re.sub('[\u2013\u2014]', '-', s)
    # s = s.replace('\u201c', '"')
    # s = s.replace('\u2019', "'")
    # s = s.replace('\u2018', "'")
    s = re.sub(r'[‘’]', "'", s)
    # s = re.sub(r'[“”]', '"', s)
    s = re.sub(r'[\u201c\u201d]', '"', s)
    s = strip_accents(s)
    s = re.sub(r'[\u0094\u0080\u00a1\u266b]', '', s)
    # s = str(s.encode('ascii', 'ignore'))  # Ignore the rest
    return s
    # return str(unicodedata.normalize('NFKD', s).encode('ascii', 'ignore'))


if __name__ == '__main__':
    from icecream import ic
    s1 = 'Meet global corruption\u2019s hidden players'
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
    s3 = "Hi. I'm here to talk about congestion, namely road congestion. Road congestion is a pervasive phenomenon. " \
         "It exists in basically all of the cities all around the world, which is a little bit surprising when you " \
         "think about it. I mean, think about how different cities are, actually. I mean, you have the typical " \
         "European cities, with a dense urban core, good public transportation mostly, not a lot of road capacity. " \
         "But then, on the other hand, you have the American cities. It's moving by itself, okay. Anyway, " \
         "the American cities: lots of roads dispersed over large areas, almost no public transportation. And then " \
         "you have the emerging world cities, with a mixed variety of vehicles, mixed land-use patterns, also rather " \
         "dispersed but often with a very dense urban core. And traffic planners all around the world have tried lots " \
         "of different measures: dense cities or dispersed cities, lots of roads or lots of public transport or lots " \
         "of bike lanes or more information, or lots of different things, but nothing seems to work. \n But all of " \
         "these attempts have one thing in common. They're basically attempts at figuring out what people should do " \
         "instead of rush hour car driving. They're essentially, to a point, attempts at planning what other people " \
         "should do, planning their life for them. \n Now, planning a complex social system is a very hard thing to " \
         "do, and let me tell you a story. Back in 1989, when the Berlin Wall fell, an urban planner in London got a " \
         "phone call from a colleague in Moscow saying, basically, \"Hi, this is Vladimir. I'd like to know, " \
         "who's in charge of London's bread supply?\" \n And the urban planner in London goes, \"What do you mean, " \
         "who's in charge of London's \u2014 I mean, no one is in charge.\" \"Oh, but surely someone must be in " \
         "charge. I mean, it's a very complicated system. Someone must control all of this.\" \n \"No. No. No one is " \
         "in charge. I mean, it basically \u2014 I haven't really thought of it. It basically organizes itself.\" \n " \
         "It organizes itself. That's an example of a complex social system which has the ability of self-organizing, " \
         "and this is a very deep insight. When you try to solve really complex social problems, the right thing to " \
         "do is most of the time to create the incentives. You don't plan the details, and people will figure out " \
         "what to do, how to adapt to this new framework. \n And let's now look at how we can use this insight to " \
         "combat road congestion. \n This is a map of Stockholm, my hometown. Now, Stockholm is a medium-sized city, " \
         "roughly two million people, but Stockholm also has lots of water and lots of water means lots of bridges " \
         "\u2014 narrow bridges, old bridges \u2014 which means lots of road congestion. And these red dots show the " \
         "most congested parts, which are the bridges that lead into the inner city. And then someone came up with " \
         "the idea that, apart from good public transport, apart from spending money on roads, let's try to charge " \
         "drivers one or two euros at these bottlenecks. \n Now, one or two euros, that isn't really a lot of money, " \
         "I mean compared to parking charges and running costs, etc., so you would probably expect that car drivers " \
         "wouldn't really react to this fairly small charge. You would be wrong. One or two euros was enough to make " \
         "20 percent of cars disappear from rush hours. Now, 20 percent, well, that's a fairly huge figure, " \
         "you might think, but you've still got 80 percent left of the problem, right? Because you still have 80 " \
         "percent of the traffic. Now, that's also wrong, because traffic happens to be a nonlinear phenomenon, " \
         "meaning that once you reach above a certain capacity threshold then congestion starts to increase really, " \
         "really rapidly. But fortunately, it also works the other way around. If you can reduce traffic even " \
         "somewhat, then congestion will go down much faster than you might think. Now, congestion charges were " \
         "introduced in Stockholm on January 3, 2006, and the first picture here is a picture of Stockholm, " \
         "one of the typical streets, January 2. The first day with the congestion charges looked like this. This is " \
         "what happens when you take away 20 percent of the cars from the streets. You really reduce congestion quite " \
         "substantially. \n But, well, as I said, I mean, car drivers adapt, right? So after a while they would all " \
         "come back because they have sort of gotten used to charges. Wrong again. It's now six and a half years ago " \
         "since the congestion charges were introduced in Stockholm, and we basically have the same low traffic " \
         "levels still. \n But you see, there's an interesting gap here in the time series in 2007. Well, " \
         "the thing is that, the congestion charges, they were introduced first as a trial, so they were introduced " \
         "in January and then abolished again at the end of July, followed by a referendum, and then they were " \
         "reintroduced again in 2007, which of course was a wonderful scientific opportunity. I mean, this was a " \
         "really fun experiment to start with, and we actually got to do it twice. And personally, I would like to do " \
         "this every once a year or so, but they won't let me do that. But it was fun anyway. \n So, we followed up. " \
         "What happened? This is the last day with the congestion charges, July 31, and you see the same street but " \
         "now it's summer, and summer in Stockholm is a very nice and light time of the year, and the first day " \
         "without the congestion charges looked like this. All the cars were back again, and you even have to admire " \
         "the car drivers. They adapt so extremely quickly. The first day they all came back. And this effect hanged " \
         "on. So 2007 figures looked like this. \n Now these traffic figures are really exciting and a little bit " \
         "surprising and very useful to know, but I would say that the most surprising slide here I'm going to show " \
         "you today is not this one. It's this one. This shows public support for congestion pricing of Stockholm, " \
         "and you see that when congestion pricing were introduced in the beginning of Spring 2006, people were " \
         "fiercely against it. Seventy percent of the population didn't want this. But what happened when the " \
         "congestion charges were there is not what you would expect, that people hated it more and more. No, " \
         "on the contrary, they changed, up to a point where we now have 70 percent support for keeping the charges, " \
         "meaning that \u2014 I mean, let me repeat that: 70 percent of the population in Stockholm want to keep a " \
         "price for something that used to be free. \n Okay. So why can that be? Why is that? Well, think about it " \
         "this way. Who changed? I mean, the 20 percent of the car drivers that disappeared, surely they must be " \
         "discontent in a way. And where did they go? If we can understand this, then maybe we can figure out how " \
         "people can be so happy with this. Well, so we did this huge interview survey with lots of travel services, " \
         "and tried to figure out who changed, and where did they go? And it turned out that they don't know " \
         "themselves. (Laughter) For some reason, the car drivers are \u2014 they are confident they actually drive " \
         "the same way that they used to do. And why is that? It's because that travel patterns are much less stable " \
         "than you might think. Each day, people make new decisions, and people change and the world changes around " \
         "them, and each day all of these decisions are sort of nudged ever so slightly away from rush hour car " \
         "driving in a way that people don't even notice. They're not even aware of this themselves. \n And the other " \
         "question, who changed their mind? Who changed their opinion, and why? So we did another interview survey, " \
         "tried to figure out why people changed their mind, and what type of group changed their minds? And after " \
         "analyzing the answers, it turned out that more than half of them believe that they haven't changed their " \
         "minds. They're actually confident that they have liked congestion pricing all along. Which means that we " \
         "are now in a position where we have reduced traffic across this toll cordon with 20 percent, and reduced " \
         "congestion by enormous numbers, and people aren't even aware that they have changed, and they honestly " \
         "believe that they have liked this all along. \n This is the power of nudges when trying to solve complex " \
         "social problems, and when you do that, you shouldn't try to tell people how to adapt. You should just nudge " \
         "them in the right direction. And if you do it right, people will actually embrace the change, and if you do " \
         "it right, people will actually even like it. Thank you. (Applause) "
    s4 = "Comics that ask \u201cwhat if?\u201d"
    s5 = "The Olympic motto is \"Citius, Altius, Fortius.\" Faster, Higher, Stronger. And athletes have fulfilled " \
         "that motto rapidly. The winner of the 2012 Olympic marathon ran two hours and eight minutes. Had he been " \
         "racing against the winner of the 1904 Olympic marathon, he would have won by nearly an hour and a half. Now " \
         "we all have this feeling that we're somehow just getting better as a human race, inexorably progressing, " \
         "but it's not like we've evolved into a new species in a century. So what's going on here? I want to take a " \
         "look at what's really behind this march of athletic progress. \n In 1936, Jesse Owens held the world record " \
         "in the 100 meters. Had Jesse Owens been racing last year in the world championships of the 100 meters, " \
         "when Jamaican sprinter Usain Bolt finished, Owens would have still had 14 feet to go. That's a lot in " \
         "sprinter land. To give you a sense of how much it is, I want to share with you a demonstration conceived by " \
         "sports scientist Ross Tucker. Now picture the stadium last year at the world championships of the 100 " \
         "meters: thousands of fans waiting with baited breath to see Usain Bolt, the fastest man in history; " \
         "flashbulbs popping as the nine fastest men in the world coil themselves into their blocks. And I want you " \
         "to pretend that Jesse Owens is in that race. Now close your eyes for a second and picture the race. Bang! " \
         "The gun goes off. An American sprinter jumps out to the front. Usain Bolt starts to catch him. Usain Bolt " \
         "passes him, and as the runners come to the finish, you'll hear a beep as each man crosses the line. (Beeps) " \
         "That's the entire finish of the race. You can open your eyes now. That first beep was Usain Bolt. That last " \
         "beep was Jesse Owens. Listen to it again. (Beeps) When you think of it like that, it's not that big a " \
         "difference, is it? And then consider that Usain Bolt started by propelling himself out of blocks down a " \
         "specially fabricated carpet designed to allow him to travel as fast as humanly possible. Jesse Owens, " \
         "on the other hand, ran on cinders, the ash from burnt wood, and that soft surface stole far more energy " \
         "from his legs as he ran. Rather than blocks, Jesse Owens had a gardening trowel that he had to use to dig " \
         "holes in the cinders to start from. Biomechanical analysis of the speed of Owens' joints shows that had " \
         "been running on the same surface as Bolt, he wouldn't have been 14 feet behind, he would have been within " \
         "one stride. Rather than the last beep, Owens would have been the second beep. Listen to it again. (Beeps) " \
         "That's the difference track surface technology has made, and it's done it throughout the running world. \n " \
         "Consider a longer event. In 1954, Sir Roger Bannister became the first man to run under four minutes in the " \
         "mile. Nowadays, college kids do that every year. On rare occasions, a high school kid does it. As of the " \
         "end of last year, 1,314 men had run under four minutes in the mile, but like Jesse Owens, Sir Roger " \
         "Bannister ran on soft cinders that stole far more energy from his legs than the synthetic tracks of today. " \
         "So I consulted biomechanics experts to find out how much slower it is to run on cinders than synthetic " \
         "tracks, and their consensus that it's one and a half percent slower. So if you apply a one and a half " \
         "percent slowdown conversion to every man who ran his sub-four mile on a synthetic track, this is what " \
         "happens. Only 530 are left. If you look at it from that perspective, fewer than ten new men per [year] have " \
         "joined the sub-four mile club since Sir Roger Bannister. Now, 530 is a lot more than one, and that's partly " \
         "because there are many more people training today and they're training more intelligently. Even college " \
         "kids are professional in their training compared to Sir Roger Bannister, who trained for 45 minutes at a " \
         "time while he ditched gynecology lectures in med school. And that guy who won the 1904 Olympic marathon in " \
         "three in a half hours, that guy was drinking rat poison and brandy while he ran along the course. That was " \
         "his idea of a performance-enhancing drug. (Laughter) \n Clearly, athletes have gotten more savvy about " \
         "performance-enhancing drugs as well, and that's made a difference in some sports at some times, " \
         "but technology has made a difference in all sports, from faster skis to lighter shoes. Take a look at the " \
         "record for the 100-meter freestyle swim. The record is always trending downward, but it's punctuated by " \
         "these steep cliffs. This first cliff, in 1956, is the introduction of the flip turn. Rather than stopping " \
         "and turning around, athletes could somersault under the water and get going right away in the opposite " \
         "direction. This second cliff, the introduction of gutters on the side of the pool that allows water to " \
         "splash off, rather than becoming turbulence that impedes the swimmers as they race. This final cliff, " \
         "the introduction of full-body and low-friction swimsuits. \n Throughout sports, technology has changed the " \
         "face of performance. In 1972, Eddy Merckx set the record for the longest distance cycled in one hour at 30 " \
         "miles, 3,774 feet. Now that record improved and improved as bicycles improved and became more aerodynamic " \
         "all the way until 1996, when it was set at 35 miles, 1,531 feet, nearly five miles farther than Eddy Merckx " \
         "cycled in 1972. But then in 2000, the International Cycling Union decreed that anyone who wanted to hold " \
         "that record had to do so with essentially the same equipment that Eddy Merckx used in 1972. Where does the " \
         "record stand today? 30 miles, 4,657 feet, a grand total of 883 feet farther than Eddy Merckx cycled more " \
         "than four decades ago. Essentially the entire improvement in this record was due to technology. \n Still, " \
         "technology isn't the only thing pushing athletes forward. While indeed we haven't evolved into a new " \
         "species in a century, the gene pool within competitive sports most certainly has changed. In the early half " \
         "of the 20th century, physical education instructors and coaches had the idea that the average body type was " \
         "the best for all athletic endeavors: medium height, medium weight, no matter the sport. And this showed in " \
         "athletes' bodies. In the 1920s, the average elite high-jumper and average elite shot-putter were the same " \
         "exact size. But as that idea started to fade away, as sports scientists and coaches realized that rather " \
         "than the average body type, you want highly specialized bodies that fit into certain athletic niches, " \
         "a form of artificial selection took place, a self-sorting for bodies that fit certain sports, and athletes' " \
         "bodies became more different from one another. Today, rather than the same size as the average elite high " \
         "jumper, the average elite shot-putter is two and a half inches taller and 130 pounds heavier. And this " \
         "happened throughout the sports world. \n In fact, if you plot on a height versus mass graph one data point " \
         "for each of two dozen sports in the first half of the 20th century, it looks like this. There's some " \
         "dispersal, but it's kind of grouped around that average body type. Then that idea started to go away, " \
         "and at the same time, digital technology - first radio, then television and the Internet - gave millions, " \
         "or in some cases billions, of people a ticket to consume elite sports performance. The financial incentives " \
         "and fame and glory afforded elite athletes skyrocketed, and it tipped toward the tiny upper echelon of " \
         "performance. It accelerated the artificial selection for specialized bodies. And if you plot a data point " \
         "for these same two dozen sports today, it looks like this. The athletes' bodies have gotten much more " \
         "different from one another. And because this chart looks like the charts that show the expanding universe, " \
         "with the galaxies flying away from one another, the scientists who discovered it call it \"The Big Bang of " \
         "Body Types.\" \n In sports where height is prized, like basketball, the tall athletes got taller. In 1983, " \
         "the National Basketball Association signed a groundbreaking agreement making players partners in the " \
         "league, entitled to shares of ticket revenues and television contracts. Suddenly, anybody who could be an " \
         "NBA player wanted to be, and teams started scouring the globe for the bodies that could help them win " \
         "championships. Almost overnight, the proportion of men in the NBA who are at least seven feet tall doubled " \
         "to 10 percent. Today, one in 10 men in the NBA is at least seven feet tall, but a seven-foot-tall man is " \
         "incredibly rare in the general population - so rare that if you know an American man between the ages of 20 " \
         "and 40 who is at least seven feet tall, there's a 17 percent chance he's in the NBA right now. (Laughter) " \
         "That is, find six honest seven footers, one is in the NBA right now. And that's not the only way that NBA " \
         "players' bodies are unique. This is Leonardo da Vinci's \"Vitruvian Man,\" the ideal proportions, " \
         "with arm span equal to height. My arm span is exactly equal to my height. Yours is probably very nearly so. " \
         "But not the average NBA player. The average NBA player is a shade under 6'7\", with arms that are seven " \
         "feet long. Not only are NBA players ridiculously tall, they are ludicrously long. Had Leonardo wanted to " \
         "draw the Vitruvian NBA Player, he would have needed a rectangle and an ellipse, not a circle and a square. " \
         "\n So in sports where large size is prized, the large athletes have gotten larger. Conversely, " \
         "in sports where diminutive stature is an advantage, the small athletes got smaller. The average elite " \
         "female gymnast shrunk from 5'3\" to 4'9\" on average over the last 30 years, all the better for their " \
         "power-to-weight ratio and for spinning in the air. And while the large got larger and the small got " \
         "smaller, the weird got weirder. The average length of the forearm of a water polo player in relation to " \
         "their total arm got longer, all the better for a forceful throwing whip. And as the large got larger, " \
         "small got smaller, and the weird weirder. In swimming, the ideal body type is a long torso and short legs. " \
         "It's like the long hull of a canoe for speed over the water. And the opposite is advantageous in running. " \
         "You want long legs and a short torso. And this shows in athletes' bodies today. Here you see Michael " \
         "Phelps, the greatest swimmer in history, standing next to Hicham El Guerrouj, the world record holder in " \
         "the mile. These men are seven inches different in height, but because of the body types advantaged in their " \
         "sports, they wear the same length pants. Seven inches difference in height, these men have the same length " \
         "legs. \n Now in some cases, the search for bodies that could push athletic performance forward ended up " \
         "introducing into the competitive world populations of people that weren't previously competing at all, " \
         "like Kenyan distance runners. We think of Kenyans as being great marathoners. Kenyans think of the Kalenjin " \
         "tribe as being great marathoners. The Kalenjin make up just 12 percent of the Kenyan population but the " \
         "vast majority of elite runners. And they happen, on average, to have a certain unique physiology: legs that " \
         "are very long and very thin at their extremity, and this is because they have their ancestry at very low " \
         "latitude in a very hot and dry climate, and an evolutionary adaptation to that is limbs that are very long " \
         "and very thin at the extremity for cooling purposes. It's the same reason that a radiator has long coils, " \
         "to increase surface area compared to volume to let heat out, and because the leg is like a pendulum, " \
         "the longer and thinner it is at the extremity, the more energy-efficient it is to swing. To put Kalenjin " \
         "running success in perspective, consider that 17 American men in history have run faster than two hours and " \
         "10 minutes in the marathon. That's a four-minute-and-58-second-per-mile pace. Thirty-two Kalenjin men did " \
         "that last October. (Laughter) That's from a source population the size of metropolitan Atlanta. \n Still, " \
         "even changing technology and the changing gene pool in sports don't account for all of the changes in " \
         "performance. Athletes have a different mindset than they once did. Have you ever seen in a movie when " \
         "someone gets an electrical shock and they're thrown across a room? There's no explosion there. What's " \
         "happening when that happens is that the electrical impulse is causing all their muscle fibers to twitch at " \
         "once, and they're throwing themselves across the room. They're essentially jumping. That's the power that's " \
         "contained in the human body. But normally we can't access nearly all of it. Our brain acts as a limiter, " \
         "preventing us from accessing all of our physical resources, because we might hurt ourselves, " \
         "tearing tendons or ligaments. But the more we learn about how that limiter functions, the more we learn how " \
         "we can push it back just a bit, in some cases by convincing the brain that the body won't be in mortal " \
         "danger by pushing harder. Endurance and ultra-endurance sports serve as a great example. Ultra-endurance " \
         "was once thought to be harmful to human health, but now we realize that we have all these traits that are " \
         "perfect for ultra-endurance: no body fur and a glut of sweat glands that keep us cool while running; narrow " \
         "waists and long legs compared to our frames; large surface area of joints for shock absorption. We have an " \
         "arch in our foot that acts like a spring, short toes that are better for pushing off than for grasping tree " \
         "limbs, and when we run, we can turn our torso and our shoulders like this while keeping our heads straight. " \
         "Our primate cousins can't do that. They have to run like this. And we have big old butt muscles that keep " \
         "us upright while running. Have you ever looked at an ape's butt? They have no buns because they don't run " \
         "upright. And as athletes have realized that we're perfectly suited for ultra-endurance, they've taken on " \
         "feats that would have been unthinkable before, athletes like Spanish endurance racer K\u00edlian Jornet. " \
         "Here's K\u00edlian running up the Matterhorn. (Laughter) With a sweatshirt there tied around his waist. " \
         "It's so steep he can't even run here. He's pulling up on a rope. This is a vertical ascent of more than 8," \
         "000 feet, and K\u00edlian went up and down in under three hours. Amazing. And talented though he is, " \
         "K\u00edlian is not a physiological freak. Now that he has done this, other athletes will follow, " \
         "just as other athletes followed after Sir Roger Bannister ran under four minutes in the mile. \n Changing " \
         "technology, changing genes, and a changing mindset. Innovation in sports, whether that's new track surfaces " \
         "or new swimming techniques, the democratization of sport, the spread to new bodies and to new populations " \
         "around the world, and imagination in sport, an understanding of what the human body is truly capable of, " \
         "have conspired to make athletes stronger, faster, bolder, and better than ever. \n Thank you very much. \n " \
         "(Applause) "
    s6 = 'K\u00edlian'
    s7 = 'There\'s spring, summer, autumn and \u0080\u0094 Voice:'
    s8 = 'It\'s something that I call ¡No MAS!'
    s9 = 'horizon \u03c4Universes'
    # print(s, s2)
    # ic(s, str(s))
    # ic(s.encode('ascii', 'ignore'))
    # ic(s.encode('utf-8', 'ignore'))
    # ic(s2.encode('ascii', 'ignore'))
    # ic(s2.encode('utf-8', 'ignore'))
    # import requests
    # res = requests.get('https://tedsummaries.com', 'html.parser')
    # ic(res.encoding)
    # for s_ in [s1, s2, s3, s4, s5, s7]:
    for s_ in [s1, s4, s7, s8, s9]:
        s_ = unicode2ascii(s_)
        print(s_)
        ic(json.dumps(s_))

    ic(strip_accents('áéíñóúü'))
    ic(strip_accents('Ramírez Sánchez'))
    ic(strip_accents(s7))
    print(unicode2ascii(s7))

    # s = unicode2ascii(s)
    # s2 = unicode2ascii(s2)
    # s3 = unicode2ascii(s3)
    # print(s)
    # print(s2)
    # print(s3)
    # ic(json.dumps(s))
    # ic(json.dumps(s2))
    # ic(json.dumps(s3))

