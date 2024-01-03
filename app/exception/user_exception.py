class UserExistException(Exception):

    email = None
    msg = '使用者已存在'

    def __init__(self, email: str) -> None:
        self.email = email


class UserNotExistException(Exception):

    email = None
    msg = '使用者不存在'

    def __init__(self, email: str) -> None:
        self.email = email
