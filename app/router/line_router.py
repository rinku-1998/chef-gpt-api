from app.extension import config
from app.service import chat_service
from fastapi import APIRouter, Request, HTTPException
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (AsyncApiClient, AsyncMessagingApi,
                                  Configuration, ReplyMessageRequest,
                                  TextMessage)
from linebot.v3.exceptions import (InvalidSignatureError)
from linebot.v3.webhooks import (MessageEvent, TextMessageContent)

configuration = Configuration(access_token=config.ACCESS_TOKEN)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(config.CHANNEL_SECRET)
router = APIRouter(tags=['line'])


@router.post('/line/callback')
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        # 取得現有資料
        chatbot = request.app.state.chatbot

        # 清除記憶
        chatbot.memory.clear()

        # 推論
        result = chatbot.invoke({'question': event.message.text})

        # 擷取輸出文字
        answer = chat_service.extract_answer(result['answer'])

        await line_bot_api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token,
                                messages=[TextMessage(text=answer)]))

    return 'OK'
