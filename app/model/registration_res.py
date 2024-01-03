from pydantic import BaseModel
from datetime import datetime


class RegistrationRes(BaseModel):

    user_id: int  # 使用者 ID
    create_time: datetime  # 建立時間
