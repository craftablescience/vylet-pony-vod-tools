import os
import webvtt
from common import DATA
from subtitle_dl import download_subtitles


if __name__ == "__main__":
    if not os.path.isdir("../in/subtitles"):
        download_subtitles()

    search = input("enter word or phrase: ")

    for stream in DATA["streams"].keys():
        path = f"../in/subtitles/{stream}.en.vtt"
        if os.path.exists(path):
            for sentence in webvtt.read(path):
                if search in sentence.text:
                    print(stream, sentence.start_time, sentence.text)
