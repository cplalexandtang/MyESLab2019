from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    JoinEvent, ImageSendMessage, MessageEvent, PostbackEvent, BeaconEvent, TextSendMessage
)
from linebot.exceptions import LineBotApiError
from manager import lineMgr
import config
import datetime

line_bot_api = LineBotApi(config.lineConfig["token"])
handler = WebhookHandler(config.lineConfig["secret"])

# Debugger
def debugger(e):
    print("------------------> Error Code: ", e.status_code)
    print("------------------> Error Message: ", e.error.message)
    print("------------------> Error Details: ", e.error.details)

@handler.add(JoinEvent)
def handle_join(event):
    if event.source.type != "group" and event.source.type != "room":
        return
    try:
        line_bot_api.reply_message(event.reply_token,
            ImageSendMessage(
                original_content_url = "https://i.imgur.com/sVW92nl.jpg",
                preview_image_url="https://i.imgur.com/sVW92nl.jpg"
            )    
        )
    except LineBotApiError as e:
        debugger(e)

@handler.add(MessageEvent)
def handle_message(event):
    print(event.message.text)
    if event.message.text == "已抽取，請稍後" or event.message.text == "Canceled. Please wait a moment.":
        return

    profile = line_bot_api.get_profile(event.source.user_id)
    message = lineMgr.parseBeacon(event, profile)

    #try:
    line_bot_api.reply_message(event.reply_token, message)
    #except LineBotApiError as e:
        #debugger(e)

@handler.add(PostbackEvent)
def handle_postback(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    message = lineMgr.parsePostback(event, profile)
    
    #try:
    line_bot_api.reply_message(event.reply_token, message)
    #except LineBotApiError as e:
        #debugger(e)

@handler.add(BeaconEvent)
def handle_beacon(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    message = lineMgr.parseBeacon(event, profile)

    #try:
    line_bot_api.reply_message(event.reply_token, message)
    #except LineBotApiError as e:
        #debugger(e)

def push_message(user_id):
    line_bot_api.push_message(user_id, TextSendMessage(text="Your turn!!!"))