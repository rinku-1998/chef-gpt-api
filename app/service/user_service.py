from app.db.token_entity import TokenEntity
from app.exception.token_exception import TokenNotExistException
from sqlalchemy.orm import Session


def get_user(token: str, session: Session) -> int:

    # 1. 檢查 Token 是否存在
    token_query = session.query(TokenEntity).filter_by(token=token).first()
    if not token_query:
        raise TokenNotExistException

    return token_query.user_id
