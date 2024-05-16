#!/usr/bin/env python3
''' Implement logging '''
import os
import re
import mysql.connector
import logging
from typing import List

pattern_dict = {
        'search': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
        'substitute': lambda x: r'\g<field>={}'.format(x)
        }

PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    ''' Return the log message obfuscated '''
    search, subst = (pattern_dict["search"], pattern_dict["substitute"])
    return re.sub(search(fields, separator), subst(redaction), message)


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' Create a connector to the Holberton database '''
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name = os.getenv("PERSONAL_DATA_DB_NAME", "holberton")
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pswd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connect = mysql.connector.vonnect(
            host=host,
            port=3306,
            user=user,
            password=pswd,
            database=name)


def get_logger() -> logging.Logger:
    ''' Create a logger '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def main():
    ''' Obtain a database connection and retrieve all rows in the users
        table and display each row under a filtered format
    '''
    fields = ["name", "email", "phone", "ssn", "password"]
    query = "SELECT {} FROM users;".format(",".join(fields))
    logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rws = cursor.fetchall()
        for row in rws:
            record = map(
                    lambda x: '{}={}'.format(x[0], x[1]),
                    zip(fields, row),
                    )
            txt = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, txt, None, None)
            log = logging.LogRecord(*args)
            logger.handle(log)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        txt = super(RedactingFormatter, self).format(record)
        out = filter_datum(self.fields, self.REDACTION, txt, self.SEPARATOR)
        return out
