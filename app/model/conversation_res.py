from pydantic import BaseModel


class ConversationRes(BaseModel):

    id: int  # 對話 ID
    title: str  # 標題
    create_time: str  # 建立時間
