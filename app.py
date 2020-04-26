# this is dev version 
from flask import Flask, request, abort
import os, json
import requests as req
from requests_oauthlib import OAuth1Session

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, MemberJoinedEvent, Event, TextSendMessage, MessageEvent
) # イベントをimport

# Twitter configuration
configs = json.load(open("config.json"))
CK = configs["TW_KEY"]
CS = configs["TW_SECRET"]
AT = configs["TW_ACCESS_TOKEN"]
ATS = configs["TW_ACCESS_SECRET"]
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/trends/available.json"
res = twitter.get(url)

app = Flask(__name__)

# Channel access token
line_bot_api = LineBotApi(
    'lFFTPplcOzcxX7wxfcSkU0ynxMpfI5WWog81SJu8XUC9KMVNaFiuStL4HN+F8O1wHRQTsGRUChKBrWjLzDOQ3mxAxBsK81PXQhQYViio72/uVCqDWWAVc1zpsgL5q9AtO0gna3mHBrWjJL8w7OqEGgdB04t89/1O/w1cDnyilFU=')
# Channel secret
handler = WebhookHandler('1c5d174f5f7da4a50680c7073a9c4d89')

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
"""
# 新しく参加したユーザに特定のメッセージを送信
@handler.add(MemberJoinedEvent)
def handler_message(event:Event):
    joined_user = event.joined.members[0] # 参加したメンバーのデータ
    user_id = joined_user.user_id # IDを取り出す
    try:
        user_prof = line_bot_api.get_profile(user_id=user_id) # 参加したメンバーのユーザ名を取得
    except LineBotApiError: # データの取得に失敗した場合
        line_bot_api.reply_message(event.reply_token, messages="ユーザデータを取得できませんでした")
    # user_name = user_prof['displayName'] # ユーザ名を取り出す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"{str(user_prof.display_name)}さん\nようこそこの学校の光へ、僕たちは君を歓迎しよう")
    )
"""
# トレンドを取得
@handler.add(MessageEvent, message=TextMessage)
def get_topic(event:Event):
    if event.message.text == 'topic':
        if res.status_code == 200:
            topics = json.loads(res.text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"{str(topics)}")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Failed to get topics")
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )




if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
