from pydantic import BaseModel, Field


class LoginReq(BaseModel):

    email: str = Field(max_length=256)  # Email
    password: str = Field(min_length=8, max_length=20)  # 密碼
