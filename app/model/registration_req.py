from pydantic import BaseModel, Field


class RegistrationReq(BaseModel):

    name: str = Field(max_length=128)  # 姓名
    email: str = Field(max_length=256)  # Email
    password: str = Field(min_length=8, max_length=20)  # 密碼
