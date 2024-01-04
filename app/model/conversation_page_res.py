from app.model.conversation_res import ConversationRes
from app.model.page_res import PageRes
from pydantic import BaseModel


class ConversationPageRes(BaseModel):

    page: PageRes  # 頁數資料
    conversations: list[ConversationRes]  # 對話列表
