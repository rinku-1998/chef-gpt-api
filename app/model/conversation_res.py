from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConversationRes(BaseModel):

    id: int  # 對話 ID
    title: Optional[str]  # 標題
    create_time: datetime  # 建立時間

    class Config:
        from_attributes = True
