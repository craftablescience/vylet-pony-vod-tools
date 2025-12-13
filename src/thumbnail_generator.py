import os
from PIL import Image, ImageDraw, ImageFont
from common import DATA, stream_to_filename


BOX_OFFSET = 64
BOX_RADIUS = 16
BOX_OUTLINE_WIDTH = 4
TEXT_OFFSET = 24
FONT_SIZE = 110

BROKEN_HEIGHT_CHARS = ['(', ')', 'H']


def draw_text_in_box(i: Image, dr: ImageDraw, d: str, f: ImageFont, bottom: bool) -> None:
    text_bbox = f.getbbox(d)
    text_width, text_height = (text_bbox[2] - text_bbox[0]), (text_bbox[3] - text_bbox[1])

    position = (BOX_OFFSET, ((i.size[1] - BOX_OFFSET - text_height) if bottom else BOX_OFFSET) + (-TEXT_OFFSET if bottom else TEXT_OFFSET) * 2)

    dr.rounded_rectangle(
        xy=(position[0] - TEXT_OFFSET, position[1] - TEXT_OFFSET + (text_height / 2), position[0] + text_width + TEXT_OFFSET, position[1] + text_height + TEXT_OFFSET + (text_height / 2)),
        radius=BOX_RADIUS,
        fill="white",
        outline="black",
        width=BOX_OUTLINE_WIDTH
    )

    for c in d:
        if c in BROKEN_HEIGHT_CHARS:
            position = (position[0], position[1] + text_height / 3)
            break

    dr.text(
        xy=position,
        text=d,
        font=f,
        fill=DATA["thumbnails"][DATA["streams"][d]["thumbnail"]]
    )


if __name__ == "__main__":
    os.makedirs("../out/thumbs", exist_ok=True)

    for stream_name, stream_data in DATA["streams"].items():
        input_path = f"../assets/thumbs/{stream_data["thumbnail"]}.jpg"
        output_path = f"../out/thumbs/{stream_to_filename(stream_name)}.jpg"
        if os.path.exists(output_path):
            continue

        image = Image.open(input_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("../assets/thumbs/Equestria.ttf", FONT_SIZE)

        draw_text_in_box(image, draw, stream_name, font, True)

        image.save(output_path, quality="web_high")
