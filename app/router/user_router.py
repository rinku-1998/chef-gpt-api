from app.db.user_entity import UserEntity
from app.db.token_entity import TokenEntity
from app.db.login_entity import LoginEntity
from app.exception.user_exception import UserExistException, UserNotExistException
from app.exception.password_exception import PasswordNotStrongException, WrongPasswordException
from app.exception.token_exception import TokenNotExistException, MissingTokenException
from app.helper.db_helper import get_session
from app.helper import password_helper
from app.model.base_res import BaseRes
from app.model.registration_req import RegistrationReq
from app.model.registration_res import RegistrationRes
from app.model.login_req import LoginReq
from app.model.login_res import LoginRes
from app.util import uuid_util, time_util
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()


@router.post('/registrations', response_model=BaseRes[RegistrationRes])
def registrations(req: RegistrationReq,
                  session: Session = Depends(get_session)):

    # 1. 檢查 Email 是否重複
    user_query = session.query(UserEntity).filter_by(email=req.email).first()
    if user_query:
        raise UserExistException(req.email)

    # 2. 檢查密碼強度
    if not password_helper.check_password(req.password):
        raise PasswordNotStrongException

    # 3. 新建使用者
    user_new = UserEntity(name=req.name,
                          email=req.email,
                          password_hash=password_helper.hash_password(
                              req.password),
                          create_time=time_util.current_time)

    session.add(user_new)
    session.commit()
    session.refresh(user_new)

    # 4. 整理回傳資料
    registration_res = RegistrationRes(user_id=user_new.id,
                                       create_time=user_new.create_time)

    res = BaseRes(data=registration_res)

    return res


@router.post('/login', response_model=BaseRes[LoginRes])
def login(req: LoginReq, session: Session = Depends(get_session)):

    # 1. 檢查使用者是否存在
    user_query = session.query(UserEntity).filter_by(email=req.email).first()
    if not user_query:
        raise UserNotExistException

    # 2. 檢查密碼
    if not password_helper.verify_password(req.password,
                                           user_query.password_hash):
        raise WrongPasswordException

    # 3. 發行 Token
    # NOTE: 使用 UUID 可以忽略重複性，所以不檢查是否已經發行過了
    token = uuid_util.gen_uuid()

    # 寫入資料庫
    now_time = time_util.current_time()
    token_new = TokenEntity(token=token,
                            user_id=user_query.id,
                            issue_time=now_time)
    login_new = LoginEntity(user_id=user_query.id, login_time=now_time)
    session.add_all([token_new, login_new])
    session.commit()

    # 4. 整理回傳資料
    login_res = LoginRes(user_id=user_query.id,
                         name=user_query.name,
                         token=token,
                         login_time=now_time)
    res = BaseRes(data=login_res)

    return res


@router.delete('/logout', response_model=BaseRes)
def logout(token: Annotated[str | None, Header()] = None,
           session: Session = Depends(get_session)):

    # 1. 檢查 Token 是否為空
    if not token:
        raise MissingTokenException

    # 2. 檢查 Token 是否存在
    token_query = session.query(TokenEntity).filter_by(token=token).first()
    if not token_query:
        raise TokenNotExistException

    # 3. 刪除 Token
    session.delete(token_query)
    session.commit()

    # 4. 整理回傳資料
    res = BaseRes()

    return res
