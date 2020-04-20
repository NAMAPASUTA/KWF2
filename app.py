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
handler = WebhookHandler('b72a8f1a406b42d25c147e63d7f794a1')

@app.route("/callback", methods=['POST'])
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
