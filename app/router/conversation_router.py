from app.db.conversation_entity import ConversationEntity
from app.db.message_entity import MessageEntity
from app.db.role_entity import RoleEntity
from app.exception.db_exception import ItemNotExistException
from app.enum.role import Role
from app.model.base_res import BaseRes
from app.model.conversation_res import ConversationRes
from app.model.conversation_page_res import ConversationPageRes
from app.model.message_req import MessageReq
from app.model.message_res import MessageRes
from app.model.message_page_res import MessagePageRes
from app.model.message_qa_res import MessageQARes
from app.model.title_res import TitleRes
from app.model.page_res import PageRes
from app.helper.db_helper import get_session
from app.service import chat_service, user_service
from app.util import time_util
from fastapi import APIRouter, Header, Depends, Request
from sqlalchemy.orm import Session
from typing import Annotated, Optional

router = APIRouter(tags=['conversation'])


@router.get('/conversations', response_model=BaseRes[ConversationPageRes])
def get_conversations(token: Annotated[Optional[str], Header()] = None,
                      page: Optional[int] = 1,
                      count: Optional[int] = 10,
                      session: Session = Depends(get_session)):

    # 1. 查詢使用者
    user_id = user_service.get_user(token, session)

    # 2. 查詢對話列表
    conversation_count = session.query(
        ConversationEntity.id).filter_by(user_id=user_id).count()
    offset = 0 if page == 1 else (page - 1) * count
    conversation_query = session.query(ConversationEntity).filter_by(
        user_id=user_id).order_by(ConversationEntity.create_time.desc()).limit(
            count).offset(offset).all()

    # 3. 整理資料
    conversation_reses = [
        ConversationRes.model_validate(_) for _ in conversation_query
    ]
    page_res = PageRes(count=count, total_count=conversation_count)

    conversation_page_res = ConversationPageRes(
        page=page_res, conversations=conversation_reses)
    res = BaseRes(data=conversation_page_res)

    return res


@router.post('/conversations', response_model=BaseRes[ConversationRes])
def create_conversation(token: Annotated[Optional[str],
                                         Header()] = None,
                        session: Session = Depends(get_session)):

    # 1. 查詢使用者
    user_id = user_service.get_user(token, session)

    # 2. 新建資料
    conversation_new = ConversationEntity(user_id=user_id,
                                          title=None,
                                          create_time=time_util.current_time())
    session.add(conversation_new)
    session.commit()
    session.refresh(conversation_new)

    # 3. 整理資料
    conversation_res = ConversationRes.model_validate(conversation_new)
    res = BaseRes(data=conversation_res)

    return res


@router.delete('/conversations/{conversation_id}', response_model=BaseRes)
def delete_conversation(conversation_id: int,
                        token: Annotated[Optional[str],
                                         Header()] = None,
                        session: Session = Depends(get_session)):

    # 1. 查詢使用者
    user_id = user_service.get_user(token, session)

    # 2. 查詢對話資料
    conversation_query = session.query(ConversationEntity).filter_by(
        id=conversation_id).first()
    if not conversation_query:
        raise ItemNotExistException

    # 3. 檢查資料是否為當前使用者的
    if conversation_query.user_id != user_id:
        raise ItemNotExistException

    # 4. 刪除訊息資料
    session.query(MessageEntity).filter_by(
        conversation_id=conversation_id).delete()
    session.commit()

    # 5. 刪除對話資料
    session.delete(conversation_query)
    session.commit()

    # 6. 整理資料
    res = BaseRes()

    return res


@router.get('/titles/{conversation_id}', response_model=BaseRes[TitleRes])
def get_title(conversation_id: int,
              token: Annotated[Optional[str], Header()] = None,
              session: Session = Depends(get_session)):

    # 1. 查詢使用者
    user_id = user_service.get_user(token, session)

    # 2. 查詢對話 ID 是否為同一個使用者
    conversation_query = session.query(ConversationEntity).filter_by(
        id=conversation_id).first()
    if not conversation_query:
        raise ItemNotExistException

    # TODO: 未來可以考慮是否要加一個操作非自己物件的例外
    if conversation_query.user_id != user_id:
        raise ItemNotExistException

    # 3. 查詢標題
    title_res = TitleRes(title=conversation_query.title)
    res = BaseRes(data=title_res)

    return res


@router.get('/messages/{conversation_id}',
            response_model=BaseRes[MessagePageRes])
def get_messages(conversation_id: int,
                 page: Optional[int] = 1,
                 count: Optional[int] = 10,
                 token: Annotated[Optional[str], Header()] = None,
                 session: Session = Depends(get_session)):

    # 1. 查詢使用者
    user_id = user_service.get_user(token, session)

    # 2. 查詢對話 ID 是否為同一個使用者
    conversation_query = session.query(ConversationEntity).filter_by(
        id=conversation_id).first()
    if not conversation_query:
        raise ItemNotExistException

    # TODO: 未來可以考慮是否要加一個操作非自己物件的例外
    if conversation_query.user_id != user_id:
        raise ItemNotExistException

    # 3. 查詢訊息列表
    message_count = session.query(
        MessageEntity.id).filter_by(conversation_id=conversation_id).count()
    offset = 0 if page == 1 else (page - 1) * count
    message_query = session.query(
        MessageEntity.id, MessageEntity.content, MessageEntity.create_time,
        RoleEntity.name.label('role')).join(
            RoleEntity, MessageEntity.role_id == RoleEntity.id).filter(
                MessageEntity.conversation_id == conversation_id).order_by(
                    MessageEntity.create_time.desc()).limit(count).offset(
                        offset).all()

    # 4. 整理資料
    message_reses = [MessageRes.model_validate(_) for _ in message_query]
    page_res = PageRes(count=count, total_count=message_count)
    message_page_res = MessagePageRes(page=page_res, messages=message_reses)

    res = BaseRes(data=message_page_res)

    return res


@router.post('/messages', response_model=BaseRes[MessageQARes])
def create_message(request: Request,
                   req: MessageReq,
                   token: Annotated[Optional[str], Header()] = None,
                   session: Session = Depends(get_session)):

    # 1. 查詢使用者
    user_id = user_service.get_user(token, session)

    # 2. 查詢對話 ID 是否為同一個使用者
    conversation_query = session.query(ConversationEntity).filter_by(
        id=req.conversation_id).first()
    if not conversation_query:
        raise ItemNotExistException

    # TODO: 未來可以考慮是否要加一個操作非自己物件的例外
    if conversation_query.user_id != user_id:
        raise ItemNotExistException

    # 3. 新建使用者訊息
    message_user = MessageEntity(conversation_id=req.conversation_id,
                                 role_id=Role.USER.value,
                                 content=req.question,
                                 create_time=time_util.current_time())

    # 4. 推論 LLM
    # 取得現有資料
    chatbot = request.app.state.chatbot
    chatbot.memory.clear()

    # 還原對話紀錄
    message_queries = session.query(MessageEntity).filter_by(
        conversation_id=req.conversation_id).order_by(
            MessageEntity.create_time.asc()).all()
    answer_idxs = [
        i for i, _ in enumerate(message_queries) if _.role_id == Role.AI.value
    ]
    for idx in answer_idxs:
        if idx - 1 < 0:
            continue

        chatbot.memory.save_context(
            {'input': message_queries[idx - 1].content},
            {'answer': message_queries[idx].content})

    # 推論
    result = chatbot({'question': req.question})
    answer = result['answer']

    # 5. 新建 AI 訊息
    message_ai = MessageEntity(conversation_id=req.conversation_id,
                               role_id=Role.AI.value,
                               content=answer,
                               create_time=time_util.current_time())

    # 6. 產生標題
    pass

    # 7. 寫入資料庫
    session.add_all([message_user, message_ai])
    session.commit()
    session.refresh(message_user)
    session.refresh(message_ai)

    # 8. 查詢角色定義資料
    role_query = session.query(RoleEntity).all()
    role_to_name = {_.id: _.name for _ in role_query}

    # 9. 整理資料
    message_qdict = message_user.__dict__
    message_qdict['role'] = role_to_name.get(Role.USER.value)
    message_adict = message_ai.__dict__
    message_adict['role'] = role_to_name.get(Role.AI.value)

    message_qres = MessageRes.model_validate(message_qdict)
    message_ares = MessageRes.model_validate(message_adict)
    message_qa_res = MessageQARes(question=message_qres, answer=message_ares)
    res = BaseRes(data=message_qa_res)

    return res
