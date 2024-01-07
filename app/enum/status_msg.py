from enum import Enum


class StatusMsg(Enum):

    # 200
    SUCCESS: str = '操作成功'

    # 400
    ITEM_NOT_EXIST: str = '物件不存在'
    USER_EXIST: str = '使用者已存在'
    USER_NOT_EXIST: str = '使用者不存在'
    PASSWORD_NOT_STRONG: str = '密碼強度不足'

    # 401
    TOKEN_MISSING: str = '缺少 Token'
    TOKEN_NOT_EXIST: str = 'Token 不存在'
    WRONG_PASSWORD: str = '密碼錯誤'

    # 404
    PAGE_NOT_FOUND: str = '查無此路由'

    # 500
    OTHER_ERROR: str = '其他錯誤'
