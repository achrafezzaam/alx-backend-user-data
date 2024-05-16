#!/usr/bin/env python3
''' Implement logging '''
import re
import logging
from typing import List

pattern_dict = {
        'search': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
        'substitute': lambda x: r'\g<field>={}'.format(x)
        }

PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    ''' Return the log message obfuscated '''
    search, subst = (pattern_dict["search"], pattern_dict["substitute"])
    return re.sub(search(fields, separator), subst(redaction), message)


def get_logger() -> logging.Logger:
    ''' Create a logger '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: str):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
                self.fields,
                self.REDACTION,
                message,
                self.SEPARATOR)
