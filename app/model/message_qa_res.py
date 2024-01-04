from app.model.message_res import MessageRes
from pydantic import BaseModel


class MessageQARes(BaseModel):

    question: MessageRes  # 問題
    answer: MessageRes  # 回答
