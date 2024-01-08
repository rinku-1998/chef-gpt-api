class EmailPatternNotCorrectException(Exception):

    msg = 'Email 格式錯誤'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
