from pydantic import BaseModel
from datetime import datetime


class MessageRes(BaseModel):

    id: int  # 訊息 ID
    role: str  # 角色
    content: str  # 內容
    create_time: datetime  # 建立時間

    class Config:
        from_attributes = True
