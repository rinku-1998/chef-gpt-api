from pydantic import BaseModel


class MessageRes(BaseModel):

    id: int  # 訊息 ID
    role: str  # 角色
    content: str  # 內容
    create_time: str  # 建立時間
