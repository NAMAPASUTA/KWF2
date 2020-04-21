from flask import Flask, request, abort
import os
import requests as req

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, MemberJoinedEvent, Event
) # イベントをimport

app = Flask(__name__)

# Channel access token
line_bot_api = LineBotApi(
    'zgW1wEtAubajZjQDsT770MZ4pLQBL9Xn4lrP9ctKXVsDQaxpw1OH/VD006yTt1CEphSTCRRNGFWqTLD45mxgy5LX7q0mehDvgoXjWthyBmMA5d5sZG22pWAjosPReY9yU0teURCQoZ9mqrI3jU2VuAdB04t89/1O/w1cDnyilFU=')
# Channel secret
handler = WebhookHandler('72c9c0e84f7427b4393262978756fe6b')

@app.route("/bot/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    
    return 'OK'

# handlerにオプションを付加して処理を付け加える
# オウム返し
@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# 新しく参加したユーザに特定のメッセージを送信
@handler.add(MemberJoinedEvent)
def handler_message(event:Event):
    joined_user = event.joined.members[0] # 参加したメンバーのデータ
    # user_id = dict(joined_user)['userId'] # IDを取り出す
    # user_prof = req.get("https://api.line.me/v2/bot/profile/"+) # 参加したメンバーのユーザ名を取得
    # user_name = (user_prof.json())['displayName']
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"ようこそこの世界へ、僕たちは君を歓迎しよう {str(joined_user)} {str(type(joined_user))}")
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
