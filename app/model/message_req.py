from pydantic import BaseModel, Field


class MessageReq(BaseModel):

    conversation_id: int  # 對話 ID
    question: str = Field(min_length=1)  # 問題
