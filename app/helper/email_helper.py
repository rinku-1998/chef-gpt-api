import re
from app.exception.email_excpetion import EmailPatternNotCorrectException


def check_email(email: str) -> bool:

    if not re.match(
            r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$',
            email):
        raise EmailPatternNotCorrectException

    return True
