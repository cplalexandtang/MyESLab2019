import sys
sys.path.append("..")

from fbmq import Attachment, Template, QuickReply, NotificationType
from api.googlePlace import getPlaces

def parseMessage(msg, profile):
    if msg.get("text"):
        return msg.get("text")

    attachments = msg.get("attachments")
    
    for item in attachments:
        typ = item.get("type")
        if typ == "location":
            lat = item.get("payload").get("coordinates").get("lat")
            lng = item.get("payload").get("coordinates").get("long")
            location = str(lat) + "," + str(lng)
            #places = getPlaces(location, radius=500)
            #print(places)
            #return wrapPlaces(places)
            return location
        else: return typ

def parsePostback(msg, profile):
    title = msg.get("title")
    if title == "同步帳號":
        return "請進入以下網址進行登入喔～只要登入一次小夏就會記得你囉！再也不用怕Facebook/Line傻傻分不清>< http://140.112.207.190:8080/web/"
    return title

def wrapPlaces(places):
    result = list()
    for place in places:
        result.append(
            Template.GenericElement(
                place.get("name"),
                subtitle = "評價：" + str(place.get("rating")) + "顆星\n照片來源：" + place.get("photo").get("source"),
                item_url = place.get("website"),
                image_url = place.get("photo").get("url"),
                buttons = [
                    Template.ButtonPostBack("營業時間", "OPENINGTIME"),
                    Template.ButtonPostBack("顯示位置", "SHOWLOC"),
                    Template.ButtonPostBack("更多資訊", "MOREINFO")
                ]
            )
        )
    if len(result) == 0: return "對不起，小夏沒有找到好吃的餐廳QQ"
    return Template.Generic(result)
