from typing import Tuple

import json5
import re
import requests


def construct_download_url(playlist: str, index: str):
    normal_url = "https://www.bilibili.com/video/" + playlist + "/?p=" + index

    ascii_url = "https%3A%2F%2Fwww.bilibili.com%2Fvideo%2F" + playlist + "%2F%3Fp%3D" + str(index)
    return "https://s4.youtube4kdownloader.com/ajax/getLinks.php?video=" + ascii_url + "&rand=" + get_decoded(normal_url)


def extract_urls(downloader_api_url, title):
    response = get_urls(downloader_api_url)
    response_json = response.json()

    result = []
    for idx, next_entity in enumerate(response_json["data"]["av"]):
        download_url = next_entity["url"].replace("[[_index_]]", str(idx))
        ext = next_entity["ext"]
        quality = next_entity["quality"]
        fps = str(next_entity["fps"])

        result.append({
            "quality": quality,
            "ext": ext,
            "fps": fps,
            "title": title + "." + ext,
            "download_url": download_url
        })

    return result


def get_urls(url):
    return requests.get(url, headers={"Content-type": "application/x-www-form-urlencoded",
                                      "User-Agent": "Mozilla/5.0 Firefox/131.0",
                                      "Accept-Encoding": "gzip, deflate, br, zstd"})


def get_decoded(url):
    return normalize(decode(url))


def decode(url, operation="dec", max_chars=3):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
    url += ''

    for _ in range(max_chars):
        enc_str = ''
        for char in url:
            pos = chars.find(char)
            if pos == -1:
                enc_str += char
            else:
                if operation == "enc":
                    enc_pos = pos + 5 if pos + 5 < len(chars) else (pos + 5) - len(chars)
                else:
                    enc_pos = pos - 5 if pos - 5 >= 0 else len(chars) + (pos - 5)

                enc_char = chars[enc_pos]
                enc_str += enc_char

        url = enc_str[::-1]

    return enc_str[::-1]


def normalize(value):
    return re.sub('[^0-9a-zA-Z]', '', value)[0: 15]


def write_to_file(file, result_list):
    for result in result_list:
        file.write(result['quality'] + "|" +
                   result['ext'] + "|" +
                   result['fps'] + "|" +
                   result['title'] + "|" +
                   result['download_url'] + "\n")

    file.flush()


if __name__ == '__main__':
    conf_file = open("conf.json5", "r")
    conf = json5.loads(conf_file.read())
    conf_file.close()

    titles = conf["titles"]
    playlist = conf["playlist"]
    file_name = conf["name"]

    file = open(file_name + ".csv", "a")

    for video_id, title in titles.items():
        print(video_id + ": " + title)

        download_url = construct_download_url(playlist, video_id)
        result_list = extract_urls(download_url, title)
        write_to_file(file, result_list)

    file.close()
