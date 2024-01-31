from app.enum.status_msg import StatusMsg
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class BaseRes(BaseModel, Generic[T]):

    msg: str = StatusMsg.SUCCESS.value  # 操作訊息
    data: Optional[T] = None  # 資料
