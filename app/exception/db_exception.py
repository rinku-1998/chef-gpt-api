class ItemNotExistException(Exception):

    msg = '找不到物件'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
