from pydantic import BaseModel
from datetime import datetime


class ConversationRes(BaseModel):

    id: int  # 對話 ID
    title: str  # 標題
    create_time: datetime  # 建立時間

    class Config:
        from_attributes = True
