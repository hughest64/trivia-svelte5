from django.conf import settings
import random

DEFAULT_WORD_FILE = settings.BASE_DIR / "game/word_lists/positive.txt"


def generate_code(word_liszt):
    three_words = []
    while len(three_words) < 3:
        word_index = random.randint(0, len(word_liszt) - 1)
        three_words.append(word_liszt[word_index])
    separator = "-"

    return separator.join(three_words)


def get_code(filename=None, max_chars=21):
    if filename is None:
        filename = DEFAULT_WORD_FILE

    word_liszt = []
    with open(filename, "r") as file_object:
        filecontents = file_object.readlines()
        for line in filecontents:
            current_place = line[:-1]
            word_liszt.append(current_place)

    code = ""
    while len(code) == 0 or len(code) > max_chars:
        code = generate_code(word_liszt)

    return code
