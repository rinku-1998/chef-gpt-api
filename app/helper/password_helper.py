import re
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_password(password: str) -> bool:

    if re.match(
            r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\!\@\#\$\%\^\&\*]).{8,20}$',
            password):
        return True

    return False


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(password_plain: str, password_hash: str) -> bool:

    return pwd_context.verify(password_plain, password_hash)
