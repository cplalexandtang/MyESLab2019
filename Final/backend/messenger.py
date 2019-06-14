from fbmq import Page, Template
from manager import fbMgr
import config

page = Page(config.messengerConfig["token"])

page.greeting("嗨~ 我是吃貨小夏，協助您創造美食小確幸！" + 
              "很高興認識你~ 點選「吃貨小夏」按鈕進入主選單，即可以探索小夏的功能和同步您的Line至Messenger帳號喔！")

page.show_persistent_menu([Template.ButtonPostBack("同步帳號", "MENU_PAYLOAD/1"),
                           Template.ButtonPostBack("美食快訊", "MENU_PAYLOAD/2"),
                           Template.ButtonPostBack("尋找餐廳", "MENU_PAYLOAD/3"),])
                          # Template.ButtonPostBack("使用說明", "MENU_PAYLOAD/4")])

@page.callback(["MENU_PAYLOAD/(.+)"])
def click_persistent_menu(payload, event):
    #click_menu = payload.split("/")[1]
    #print("you clicked %s menu" % click_menu)
    print("fuck")

@page.handle_message
def message_handler(event):
    sender_id = event.sender_id
    message = fbMgr.parseMessage(event.message, page.get_user_profile(sender_id))
    page.send(sender_id, message)

@page.handle_postback
def postback_handler(event):
    sender_id = event.sender_id
    message = fbMgr.parsePostback(event.postback, page.get_user_profile(sender_id))
    page.send(sender_id, message)

@page.handle_echo
def echo_handler(event):
    # This callback will occur when a message has been sent by your page
    pass

@page.handle_delivery
def delivery_handler(event):
    # This callback will occur when a message a page has sent has been delivered
    pass

@page.handle_read
def read_handler(event):
    # This callback will occur when a message a page has sent has been read by the user
    pass
