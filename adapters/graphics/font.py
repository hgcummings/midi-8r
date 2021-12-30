import json

font_path = __file__.replace(".py", ".json")

with open(font_path, encoding="utf8") as f:
    font = json.load(f)

gap = [[0]]

def render_line(display, offset_x, offset_y, text, colour):
    for text_char in text:
        glyph = font["glyphs"][""]
        if (font["glyphs"][text_char]):
            glyph = font["glyphs"][text_char]
        else:
            print("Missing character " + text_char)

        for y, row in enumerate(glyph["pixels"]):
            for x, pixel in enumerate(row):
                if (pixel == 1):
                    display.set_pixel(
                        x + offset_x,
                        y + offset_y + glyph["offset"],
                        colour[0],
                        colour[1],
                        colour[2])

        offset_x += len(glyph["pixels"][0]) + 1
