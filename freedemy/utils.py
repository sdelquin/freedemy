import functools
import re

import logzero

import settings


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
    logger = logzero.logger
    logger.setLevel(logzero.DEBUG)
    return logger
