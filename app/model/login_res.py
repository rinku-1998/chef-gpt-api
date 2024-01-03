from pydantic import BaseModel
from datetime import datetime


class LoginRes(BaseModel):

    user_id: int  # 使用者 ID
    name: str  # 使用者名字
    token: str  # Token
    login_time: datetime  # 登入時間
