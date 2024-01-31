from pydantic import BaseModel
from typing import Optional


class TitleRes(BaseModel):

    title: Optional[str]  # 標題
