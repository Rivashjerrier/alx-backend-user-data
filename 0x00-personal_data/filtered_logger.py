#!/usr/bin/env python3
"""
filtered_logger.py module
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    filter_datum returns the log message obfuscated
    """
    for item in fields:
        message = re.sub(item+'=.*?'+separator,
                         item+'='+redaction+separator, message)
    return message
