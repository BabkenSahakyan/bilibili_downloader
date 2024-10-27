import json
import urllib.request
import csv
import os


def read_url(quality, ext):
    result = []
    with open("csv_output.csv", "r") as urls_file:
        lines = csv.reader(urls_file, delimiter='|')
        for line in lines:
            if line[0] == quality and line[1] == ext:
                result.append(line[3::])

    return result


if __name__ == '__main__':
    conf_file = open("conf.json", "r")
    conf = json.loads(conf_file.read())
    conf_file.close()

    folder = conf["name"]
    os.makedirs(folder, exist_ok=True)

    for title, url in read_url(conf["preferred_quality"], conf["preferred_ext"]):
        print(title + " " + url)
        urllib.request.urlretrieve(url, folder + "/" + title)
