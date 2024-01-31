import logging
import sys
from app.extension import SessionLocal
from app.exception_handler import attach_exception_handlers
from app.cors_middleware import add_cors_middleware
from app.logging_handler import format_record, InterceptHandler
from app.service import chat_service
from fastapi import FastAPI
from loguru import logger


def create_app() -> FastAPI:

    # 1. 建立物件
    app = FastAPI(title='Chef GPT API', version='0.1.0')

    # 2. 日誌
    # 格式
    logger.configure(handlers=[{
        'sink': sys.stdout,
        'level': logging.DEBUG,
        'format': format_record
    }])

    # Uvicorn
    logging.getLogger().handlers = [InterceptHandler()]
    logging.getLogger('uvicorn.access').handlers = [InterceptHandler()]

    # 新增儲存位置
    logger.add('logs/run.log',
               rotation='500MB',
               encoding='utf-8',
               enqueue=True,
               retention='15 days')

    # 3. 路由
    from app.router.user_router import router as user_router
    from app.router.conversation_router import router as conversation_router
    from fastapi import APIRouter

    root_router = APIRouter(prefix='/api/v1')
    root_router.include_router(user_router)
    root_router.include_router(conversation_router)
    app.include_router(root_router)

    # 4. 例外攔截
    app = attach_exception_handlers(app)

    # 5. Middleware
    app = add_cors_middleware(app)

    # 6. 聊天模型
    chatbot = chat_service.build_chatbot()
    app.state.chatbot = chatbot

    return app
