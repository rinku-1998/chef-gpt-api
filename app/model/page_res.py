from pydantic import BaseModel


class PageRes(BaseModel):

    total_count: int  # 資料總筆數
    total_page: int = 0  # 總頁數

    def __init__(self, count: int, **kwargs):

        super().__init__(**kwargs)
        if self.total_count > 0:
            self.total_page = (self.total_count // count) + 1
