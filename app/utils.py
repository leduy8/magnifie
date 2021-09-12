import email_validator
import re
from datetime import datetime


def validate_mail(email):
    try:
        email_validator.validate_email(email)
        return True
    except:
        return False


def is_valid_url(url):
    # Regex to check valid URL
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")

    # Compile the ReGex
    compiler = re.compile(regex)

    # Return False if url is empty
    if url == None:
        return False

    # Return if the string matched the ReGex
    if re.search(compiler, url):
        return True
    return False


def validate_date(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except ValueError:
        return False
