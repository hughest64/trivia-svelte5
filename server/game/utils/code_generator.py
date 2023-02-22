# code_generator.py
"""
Functions used for auto-generating a team password.
"""

from django.conf import settings
import random


def generate_code(word_liszt, sep="-"):
    three_words = []
    while len(three_words) < 3:
        word_index = random.randint(0, len(word_liszt) - 1)
        three_words.append(word_liszt[word_index])

    return sep.join(three_words)


def get_code(word_liszt=None, max_chars=21):
    if word_liszt is None:
        word_liszt = settings.WORD_LISZT

    code = ""
    while len(code) == 0 or len(code) > max_chars:
        code = generate_code(word_liszt)

    return code
