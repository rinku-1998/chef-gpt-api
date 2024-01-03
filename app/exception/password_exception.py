class WrongPasswordException(Exception):

    msg = '密碼錯誤'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PasswordNotStrongException(Exception):

    msg = '密碼強度不足'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
