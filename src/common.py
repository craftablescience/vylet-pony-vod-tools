import json


with open("../assets/data.json") as data:
    DATA = json.load(data)


def get_stream_url(date: str, prefer_reupload: bool = False) -> str | None:
    if date in DATA["streams"]:
        if "availability" in DATA["streams"][date]:
            if DATA["streams"][date]["availability"] is None:
                return None
            return DATA["streams"][date][f"url_{DATA["streams"][date]["availability"]}"]
        if prefer_reupload:
            return DATA["streams"][date]["url_reupload"]
        return DATA["streams"][date]["url_original"]
    return None


def get_stream_url_from_source(date: str, source: str) -> str | None:
    if date in DATA["streams"]:
        if "availability" in DATA["streams"][date] and (DATA["streams"][date]["availability"] is None or DATA["streams"][date]["availability"] != source):
            return None
        return DATA["streams"][date][f"url_{source}"]
    return None


def stream_to_filename(stream: str) -> str:
    return stream \
        .replace("(", "_") \
        .replace(")", "_")
