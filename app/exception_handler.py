from app.enum.status_msg import StatusMsg
from app.exception.db_exception import ItemNotExistException
from app.exception.user_exception import UserExistException, UserNotExistException
from app.exception.password_exception import PasswordNotStrongException, WrongPasswordException
from app.exception.token_exception import TokenNotExistException, MissingTokenException
from app.exception.email_excpetion import EmailPatternNotCorrectException
from app.model.base_res import BaseRes
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def attach_exception_handlers(app: FastAPI) -> FastAPI:

    # Request 錯誤例外
    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
            request: Request,
            exception: RequestValidationError) -> JSONResponse:

        # 1. 格式化錯誤訊息
        msg = ''
        for error in exception.errors():

            location = error.get('loc')[0]
            field_name = error.get('loc')[1]

            msg += f'Request {location} 缺少 {field_name}，'

        # 2. 整理資料
        res = BaseRes(msg=msg)

        return JSONResponse(jsonable_encoder(res), status_code=400)

    # 使用者已存在
    @app.exception_handler(UserExistException)
    async def user_exist_exception_handler(
            request: Request, exception: UserExistException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.USER_EXIST.value)

        return JSONResponse(jsonable_encoder(res), status_code=400)

    # 使用者不存在
    @app.exception_handler(UserNotExistException)
    async def user_not_exist_exception_handler(
            request: Request,
            exception: UserNotExistException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.USER_NOT_EXIST.value)

        return JSONResponse(jsonable_encoder(res), status_code=400)

    # 密碼強度不足
    @app.exception_handler(PasswordNotStrongException)
    async def password_not_strong_exception_handler(
            request: Request,
            exception: PasswordNotStrongException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.PASSWORD_NOT_STRONG.value)

        return JSONResponse(jsonable_encoder(res), status_code=400)

    # 密碼錯誤
    @app.exception_handler(WrongPasswordException)
    async def wrong_password_exception_handler(
            request: Request,
            exception: WrongPasswordException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.WRONG_PASSWORD.value)

        return JSONResponse(jsonable_encoder(res), status_code=400)

    # Token 不存在
    @app.exception_handler(TokenNotExistException)
    async def token_not_exist_exception_handler(
            request: Request,
            exception: TokenNotExistException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.TOKEN_NOT_EXIST.value)

        return JSONResponse(jsonable_encoder(res), status_code=401)

    # 缺少 Token
    @app.exception_handler(MissingTokenException)
    async def missing_token_exception_handler(
            request: Request,
            exception: MissingTokenException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.TOKEN_MISSING.value)

        return JSONResponse(jsonable_encoder(res), status_code=401)

    # 物件不存在
    @app.exception_handler(ItemNotExistException)
    async def item_not_exist_exception_handler(
            request: Request,
            exception: ItemNotExistException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.ITEM_NOT_EXIST.value)

        return JSONResponse(jsonable_encoder(res), status_code=400)

    # Email 格式錯誤
    @app.exception_handler(EmailPatternNotCorrectException)
    async def email_pattern_not_correct_exception_handler(
            request: Request,
            exception: EmailPatternNotCorrectException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.EMAIL_PATTERN_NOT_CORRECT.value)

        return JSONResponse(jsonable_encoder(res), status_code=400)

    # 404
    @app.exception_handler(status.HTTP_404_NOT_FOUND)
    async def page_not_found_exception_handler(
            request: Request, exception: HTTPException) -> JSONResponse:

        res = BaseRes(msg=StatusMsg.PAGE_NOT_FOUND.value)

        return JSONResponse(jsonable_encoder(res), status_code=404)

    # 全局例外
    @app.exception_handler(Exception)
    async def base_exception_handler(request: Request,
                                     exception: Exception) -> JSONResponse:

        msg = f'{StatusMsg.OTHER_ERROR.value}, {str(exception)}'
        res = BaseRes(msg=msg)
        return JSONResponse(jsonable_encoder(res), status_code=500)

    return app
