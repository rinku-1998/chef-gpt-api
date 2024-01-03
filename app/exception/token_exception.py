class TokenNotExistException(Exception):

    msg = 'Token 不存在'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MissingTokenException(Exception):

    msg = '缺少 Token'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
