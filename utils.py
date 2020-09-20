import functools
import re


@functools.lru_cache
def get_compiled_regex(words: tuple):
    pattern = "|".join([fr"\b{word}\b" for word in words])
    return re.compile(pattern, re.I)
