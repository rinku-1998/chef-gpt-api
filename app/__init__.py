from fastapi import FastAPI
from app.extension import SessionLocal
from app.exception_handler import attach_exception_handlers
from app.cors_middleware import add_cors_middleware


def create_app() -> FastAPI:

    # 1. 建立物件
    app = FastAPI(title='Chef GPT API', version='0.1.0')

    # 2. 路由
    from app.router.user_router import router as user_router
    from app.router.conversation_router import router as conversation_router

    app.include_router(user_router)
    app.include_router(conversation_router)

    # 3. 例外攔截
    app = attach_exception_handlers(app)

    # 4. Middleware
    app = add_cors_middleware(app)

    return app
