#!/usr/bin/env python3
"""
filtered_logger.py module
"""

import re
from typing import List
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filter_datum returns the log message obfuscated
    """
    for item in fields:
        message = re.sub(item+'=.*?'+separator,
                         item+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Returns a logging object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger
