from pydantic import BaseModel


class PageRes(BaseModel):

    total_count: int  # 資料總筆數
