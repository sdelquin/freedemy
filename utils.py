import functools
import re

import logzero

import settings

LANGUAGE_FLAGS = {
    'af': '🇿🇦',
    'ar': '🇦🇪',
    'as': '🇮🇳',
    'az': '🇦🇿',
    'be': '🇧🇾',
    'bg': '🇧🇬',
    'bn': '🇮🇳',
    'bs': '🇧🇦',
    'cs': '🇨🇿',
    'da': '🇩🇰',
    'de': '🇩🇪',
    'el': '🇬🇷',
    'en': '🇺🇸',
    'es': '🇪🇸',
    'et': '🇪🇪',
    'fi': '🇫🇮',
    'fr': '🇫🇷',
    'gu': '🇮🇳',
    'he': '🇮🇱',
    'hi': '🇮🇳',
    'hr': '🇭🇷',
    'hu': '🇭🇺',
    'hy': '🇦🇲',
    'id': '🇮🇩',
    'is': '🇮🇸',
    'it': '🇮🇹',
    'ja': '🇯🇵',
    'ka': '🇬🇪',
    'kk': '🇰🇿',
    'kn': '🇮🇳',
    'ko': '🇰🇷',
    'ks': '🇮🇳',
    'ku': '🇹🇷',
    'ky': '🇰🇬',
    'lt': '🇱🇹',
    'lv': '🇱🇻',
    'mk': '🇲🇰',
    'ml': '🇮🇳',
    'mr': '🇮🇳',
    'ms': '🇲🇾',
    'mt': '🇲🇹',
    'nb': '🇳🇴',
    'nl': '🇳🇱',
    'nn': '🇳🇴',
    'or': '🇮🇳',
    'pa': '🇮🇳',
    'pl': '🇵🇱',
    'pt': '🇵🇹',
    'ro': '🇷🇴',
    'ru': '🇷🇺',
    'sa': '🇮🇳',
    'sl': '🇸🇮',
    'sq': '🇦🇱',
    'sr': '🇷🇸',
    'sv': '🇸🇪',
    'ta': '🇮🇳',
    'te': '🇮🇳',
    'th': '🇹🇭',
    'tr': '🇹🇷',
    'uk': '🇺🇦',
    'vi': '🇻🇳',
    'zh': '🇨🇳',
}


@functools.lru_cache
def get_compiled_regex(words: tuple):
    pattern = "|".join([fr"\b{word}\b" for word in words])
    return re.compile(pattern, re.I)


def init_logger():
    console_logformat = (
        '%(color)s%(levelname)-8s %(asctime)s %(module)s:%(lineno)d%(end_color)s> '
        '%(message)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger
