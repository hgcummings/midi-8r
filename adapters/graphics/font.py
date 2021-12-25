import json
import os

from functools import reduce

script_dir = os.path.dirname(__file__)
font_path = os.path.join(script_dir, "font.json")

with open(font_path) as f:
    font = json.load(f)

gap = [[0]]

def render_line(text, colour):
    characters = []
    max_height = 0
    for i, text_char in enumerate(text):
        glyph = font["glyphs"][""]
        if (font["glyphs"][text_char]):
            glyph = font["glyphs"][text_char]
        else:
            print("Missing character " + text_char)

        blank_row = [[0] for _ in glyph["pixels"][0]]
        new_character = [blank_row for _ in range(glyph["offset"])]        
        for row in glyph["pixels"]:
            new_character.append(row)
        max_height = max(max_height, len(new_character))
        if i > 0:
            characters.append(gap)
        characters.append(new_character)

    def append_char(line, char):
        blank_row = [[0] for _ in char[len(char) - 1]]
        for i in range(max_height):
            row = blank_row if i >= len(char) else char[i]
            line[i] += [colour if p == 1 else (0,0,0) for p in row]
        return line
        
    return reduce(append_char, characters, [[] for _ in range(max_height)])