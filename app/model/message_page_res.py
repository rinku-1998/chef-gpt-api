from model.message_res import MessageRes
from model.page_res import PageRes
from pydantic import BaseModel


class MessagePageRes(BaseModel):

    page: PageRes  # 頁數資料
    messages: list[MessageRes]  # 對話列表
