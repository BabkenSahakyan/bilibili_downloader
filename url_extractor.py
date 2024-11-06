import json5
import re
import requests


def construct_download_url(playlist: str, index: str):
    normal_url = "https://www.bilibili.com/video/" + playlist + "/?p=" + index

    ascii_url = "https%3A%2F%2Fwww.bilibili.com%2Fvideo%2F" + playlist + "%2F%3Fp%3D" + str(index)
    return "https://s4.youtube4kdownloader.com/ajax/getLinks.php?video=" + ascii_url + "&rand=" + get_decoded(normal_url)


def extract_urls(downloader_api_url, video_index, csv_output_file, curl_output_file, titles: dict):
    response = get_urls(downloader_api_url)
    response_json = response.json()

    for idx, next_entity in enumerate(response_json["data"]["av"]):
        download_url = next_entity["url"].replace("[[_index_]]", str(idx))
        title = str(titles[video_index])
        ext = next_entity["ext"]
        quality = next_entity["quality"]
        fps = str(next_entity["fps"])

        curl_output_file.write("curl --output '" +
                               titles[video_index] + "_" + quality + "_." + ext + "' " +
                               download_url + "\n")

        csv_output_file.write(quality + "|" +
                              ext + "|" +
                              fps + "|" +
                              title + "." + ext + "|" +
                              download_url + "\n")


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


if __name__ == '__main__':
    conf_file = open("conf.json5", "r")
    conf = json5.loads(conf_file.read())
    conf_file.close()

    titles = conf["titles"]
    playlist = conf["playlist"]
    name = conf["name"]

    csv_output_file = open(name + ".csv", "w")
    curl_output_file = open(name + ".txt", "w")

    for video_id, name in titles.items():
        print(video_id + ": " + name)

        download_url = construct_download_url(playlist, video_id)
        extract_urls(download_url, video_id, csv_output_file, curl_output_file, titles)

    curl_output_file.close()
    csv_output_file.close()
