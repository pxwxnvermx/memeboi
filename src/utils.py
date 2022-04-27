import configparser

import requests
import youtube_dl


def get_file_type(url):
    response = requests.head(url=url, allow_redirects=True)

    if "text/html" in response.headers.get("Content-Type", 0):
        url = download_video(url)
        response = requests.head(url=url, allow_redirects=True)

    if "video" in response.headers.get("Content-Type"):
        type = "video"
    elif "image" in response.headers.get("Content-Type"):
        type = "image"


def download_video(url):
    ydl = youtube_dl.YoutubeDL({"quiet": True, "no_warnings": True})

    with ydl:
        result = ydl.extract_info(url, download=False)

    if result.get("entries"):
        result = [res["url"] for res in result["entries"]][1]
    else:
        result = result.get("url")

    return result


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    return config
