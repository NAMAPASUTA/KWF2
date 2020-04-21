from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

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

@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    
    profile = line_bot_api.get_profile(event.source.user_id)
    status_msg = profile.status_message
    if status_msg != "None":
        # LINEに登録されているstatus_messageが空の場合は、"なし"という文字列を代わりの値とする
        status_msg = "なし"

    messages = TemplateSendMessage(alt_text="Buttons template",
                                   template=ButtonsTemplate(
                                       thumbnail_image_url=profile.picture_url,
                                       title=profile.display_name,
                                       text=f"User Id: {profile.user_id[:5]}...\n"
                                            f"Status Message: {status_msg}",
                                       actions=[MessageAction(label="成功", text="次は何を実装しましょうか？")]))

    line_bot_api.reply_message(event.reply_token, messages=messages)


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)