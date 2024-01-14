from pydantic import BaseModel


class TitleRes(BaseModel):

    title: str | None  # 標題
