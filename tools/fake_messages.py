import os
import re
import json

names = []
news = []


def fix_names():
    with open('english_names.txt') as f:
        # skip first line
        f.readline()
        names.extend([l.split()[1] for l in f])

        print(type(names[0]))
        with open('fixed_names.txt', 'w') as f2:
            f2.write('\n'.join(names))


def fix_news():
    with open('english_news.txt') as f:
        content = f.read()
        news.extend([l.strip() for l in content.split('.')])

        print(type(news[0]))
        # print(len(news))
        # for line in lines:
        # print(line)


if __name__ == "__main__":
    fix_names()
    fix_news()
    print(len(names))
    print(len(news))
    msgs = list(zip(names, news))
    dt = []
    for (a, b) in msgs:
        a and b and dt.append({
            "topic": a,
            "message": b
        })
    with open('messages.json', 'w') as f:
        json.dump(dt, f, indent='  ')
