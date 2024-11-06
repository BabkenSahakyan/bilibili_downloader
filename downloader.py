import json5
import urllib.request
import csv
import os


def read_url(name, quality, ext):
    result = []
    with open(name + ".csv", "r") as urls_file:
        lines = csv.reader(urls_file, delimiter='|')
        for line in lines:
            if line[0] == quality and line[1] == ext:
                result.append(line[3::])

    return result


if __name__ == '__main__':
    conf_file = open("conf.json5", "r")
    conf = json5.loads(conf_file.read())
    conf_file.close()

    name = conf["name"]
    os.makedirs(name, exist_ok=True)

    for title, url in read_url(name, conf["preferred_quality"], conf["preferred_ext"]):
        print(title + " " + url)
        urllib.request.urlretrieve(url, name + "/" + title)
