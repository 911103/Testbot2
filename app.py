# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('eVAHESVfOWguGISa+Ye8fNAWOUGAJ75syoKXrZ3/N8Avz4Dc0pw8hA100mf4xzUXq8SCBb61SUz9/xdYy3UCHev+kXA2QznzDeQf53B0CWDgLb8l4+rMBoLsEsWVGzyp01NUQTJFHAD7l8leF4NrmAdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('564b63836ccb1084a63387b47d24f43a')

line_bot_api.push_message('U8b2d0e1e226d3a7b6f65d59339b61481', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)