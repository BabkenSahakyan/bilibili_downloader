from urllib.error import HTTPError
import datetime
import urllib.request
import csv
import os

import util


def read_url(name):
    result = []
    with open(name + ".csv", "r") as urls_file:
        lines = csv.reader(urls_file, delimiter='|')
        for line in lines:
            result.append(line[3::])

    return result


if __name__ == '__main__':
    conf = util.read_conf()

    name = conf["name"]
    os.makedirs(name, exist_ok=True)

    start_idx = conf.get("start", 0)
    increment = conf.get("increment", 1)
    next_idx = start_idx

    print("start: %s, increment: %s" % (start_idx, increment))

    urls = read_url(name)
    for idx, (title, url) in enumerate(urls):
        if idx == next_idx:
            print("%s: %s %s" % (str(datetime.datetime.now()), title, url))
            try:
                urllib.request.urlretrieve(url, name + "/" + title)
            except HTTPError:
                print("skipping " + title)
            finally:
                next_idx += increment
