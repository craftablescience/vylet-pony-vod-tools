import chat_downloader
import colorsys
import os
import yt_dlp
from common import DATA, get_stream_url, get_stream_url_from_source, stream_to_filename


def download_subtitles_for(stream: str, reupload: bool = False) -> bool:
    url = get_stream_url(stream, reupload)
    if not url:
        return False

    os.makedirs("../in/subtitles", exist_ok=True)

    output_stem = f"../in/subtitles/{stream_to_filename(stream)}"
    if os.path.isfile(f"{output_stem}.en.vtt.notfound"):
        return True

    if not os.path.isfile(f"{output_stem}.en.vtt"):
        download_options = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": [
                "en.*",
            ],
            "subtitlesformat": "vtt",
            "outtmpl": output_stem,
        }

        try:
            with yt_dlp.YoutubeDL(download_options) as ydl:
                ydl.download([url])
            if os.path.isfile(f"{output_stem}.en-orig.vtt"):
                os.remove(f"{output_stem}.en-orig.vtt")
            if not reupload and not os.path.isfile(f"{output_stem}.en.vtt"):
                return download_subtitles_for(stream, True)
        except Exception as e:
            print(f"Error downloading subtitles: {e}")
            return False

    return True


def download_subtitles() -> None:
    for stream in DATA["streams"].keys():
        if not download_subtitles_for(stream):
            with open(f"../in/subtitles/{stream_to_filename(stream)}.en.vtt.notfound", "w") as _:
                pass


def colorize_username(username: str) -> str:
    username_hash = 0
    for i in range(len(username)):
        username_hash = ord(username[i]) + ((username_hash << 5) - username_hash)
    rgb = [((username_hash >> (i * 8)) & 0xFF) / 255.0 for i in range(3)]
    hsv = [*colorsys.rgb_to_hsv(*rgb)]
    hsv[1] = 0.5 if hsv[1] < 0.5 else 0.9 if hsv[1] > 0.9 else hsv[1]
    hsv[2] = 0.5 if hsv[2] < 0.5 else 0.9 if hsv[2] > 0.9 else hsv[2]
    rgb = [int(v * 255) for v in colorsys.hsv_to_rgb(*hsv)]
    color = "#"
    for i in range(3):
        color += f"{rgb[i]:0>2x}"
    return color


def download_live_chat_for(stream: str) -> bool:
    url = get_stream_url_from_source(stream, "original")
    if not url:
        return False

    os.makedirs("../in/live_chat", exist_ok=True)

    output_csv = f"../in/live_chat/{stream_to_filename(stream)}.csv"
    if os.path.isfile(f"{output_csv}.notfound"):
        return True

    if not os.path.isfile(output_csv):
        try:
            chat = chat_downloader.ChatDownloader().get_chat(url)
            with open(output_csv, "w") as csv:
                csv.write("time,user_name,user_color,message\n")
                csv.writelines([
                    f"{message["time_in_seconds"]},{message["author"]["name"]},{colorize_username(message["author"]["name"])},{message["message"]}\n"
                    for message in chat
                ])
        except Exception as e:
            print(f"Error downloading live chat: {e}")
            os.remove(output_csv)
            return False

        os.makedirs("../out/live_chat", exist_ok=True)

        output_ytt = f"../out/live_chat/{stream_to_filename(stream)}.ytt"
        if not os.path.isfile(output_ytt):
            return os.system(f"../ext/subchat/build/subtitles_generator -c ../assets/live_chat/config.ini -i \"{output_csv}\" -o \"{output_ytt}\" -u sec") == 0

    return True


def download_live_chat() -> None:
    for stream in DATA["streams"].keys():
        if not download_live_chat_for(stream):
            with open(f"../in/live_chat/{stream_to_filename(stream)}.csv.notfound", "w") as _:
                pass


if __name__ == "__main__":
    download_subtitles()
    download_live_chat()
