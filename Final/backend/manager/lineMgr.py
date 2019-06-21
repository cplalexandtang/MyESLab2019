import sys
import requests
import json
import random
import datetime

#sys.path.append("..")

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
)

import api.number

def parseMessage(event, profile):
    if event.message.type == "text":
        msg = event.message.text
        src = event.source.type
        return TextSendMessage(text=msg)

    else: return TextSendMessage(text=str(event.type))

def parsePostback(event, profile):
    if event.postback.data == "number":
        queue = api.number.UserQueue()
        try:
            num = queue.push(profile.user_id, profile.display_name)
        except:
            return TextSendMessage(text="You are already in line. Please cancel your number first.")

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text="您的號碼是：" + str(num), weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            TextComponent(text='歡迎光臨您的理財好夥伴，嘎啦嘎啦嘎啦', size='sm', color='#999999', margin='md', flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='分行',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text='臺北市信義分行',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='營業時間',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(label="取消抽號", data="cancel", text="Canceled. Please wait a moment.") #URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(label="現在進度", data="progress")
                    )
                ]
            ),
        )

        return FlexSendMessage(alt_text="號碼牌", contents=bubble)
    
    elif event.postback.data == "cancel":
        queue = api.number.UserQueue()
        queue.pop(uuid = profile.user_id)

        return TextSendMessage(text="Deleted")

    elif event.postback.data == "progress":
        queue = api.number.UserQueue()
        return TextSendMessage(text="There are {} people waiting in front of you".format(len(queue.waitingList()) - 1))

def parseBeacon(event, profile):
    '''reply = "現在時間: {}\n Hardware id: {}\n Device message: {}\n 你正在: {}".format(
                datetime.datetime.fromtimestamp(event.timestamp/1000).strftime("%Y-%m-%d %H:%M:%S"),
                event.beacon.hwid,
                event.beacon.dm,
                event.beacon.type
                )'''
    
    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.hsbc.com.tw/etc/designs/dpws/common/social/logo/Square-1200x1200px.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://www.hsbc.com.tw/', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text="NTUEE Bank", weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            TextComponent(text='歡迎光臨您的理財好夥伴，嘎啦嘎啦嘎啦', size='sm', color='#999999', margin='md', flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='分行',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text='明達305',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='營業時間',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(label="抽號碼牌", data="number", text="已抽取，請稍後") #URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='優惠訊息', uri="https://example.com")
                    )
                ]
            ),
        )

    return FlexSendMessage(alt_text="歡迎光臨", contents=bubble)
