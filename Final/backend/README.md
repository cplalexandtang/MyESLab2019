# Line Beacon

This is the development version of the 2019 NTUEE ESLab.

這是2019 NTUEE ESLab的開發版本

# Line 

## Profile

    {
        "displayName":"湯大由",
        "pictureUrl":"http://dl.profile.line-cdn.net/0m04dc902672512b6bb869019876af85c7c18331680991",
        "statusMessage":null,
        "userId":"U781764583123e034919f908c837cfeb9"
    }

## Message Event

### Text

    {
        "message": {
            "id":"8297553232947",
            "text":"你好",
            "type":"text"
        },
        "replyToken":"3d9d6f576a4e45b7bb37c6c9b604b78d",
        "source": {
            "type":"user",
            "userId":"U789b69rffrgrg4g63e099f908c837cfeb9"
        },
        "timestamp":1532163731990,
        "type":"message"
    }

### Sticker

    {
        "message": {
            "id":"8297569291704",
            "packageId":"11537",
            "stickerId":"52002735",
            "type":"sticker"
        },
        "replyToken":"fb970982eab942f2967b1cbded40ec87",
        "source": {
            "type":"user",
            "userId":"U7063e094919f4rf4rf4rf4rf908c837cfeb9"
        },
        "timestamp":1532163963168,
        "type":"message"
    }

### Image

    {
        "message": {
            "id":"8297614885410",
            "type":"image"
        },
        "replyToken":"17117a70d1024bb8aacf2e9816844dfa",
        "source": {
            "type":"user",
            "userId":"U789b694f4rfr4f4rf4rf4r31063e09cfeb9"
        },
        "timestamp":1532164624265,
        "type":"message"
    }

### Location

    {
        "message": {
            "address":"某個地址",
            "id":"8297554024266",
            "latitude":25.05663201757178,
            "longitude":121.51982732463144,
            "title":null,
            "type":"location"
        },
        "replyToken":"e4aabcf0770948c4abb3a78827c76e32",
        "source": {
            "type":"user",
            "userId":"U789b69431063e094rf4rf4fr4f4f4rfb9"
        },
        "timestamp":1532163743292,
        "type":"message"
    }

## Join Event

    {
        "replyToken":"03ea5e9aa7b84310885fa193c70abcf1",
        "source": {
            "groupId":"C2cbb58f495faac594rf4rf4rfr4f4r86",
            "type":"group",
            "userId":null
        },
        "timestamp":1532191372839,
        "type":"join"
    }

## Postback Event

    {
        "replyToken": "b7e5986f3b28481088fcd13c85f89c32", 
        "postback": {
            "data": "OPENINGTIME"
        }, 
        "source": {
            "type": "user", 
            "userId": "U789b694310634rf4rfr4f4rf4rb9"
        }, 
        "timestamp": 1532334232240, 
        "type": "postback"
    }

## Beacon Event

    {
        "beacon": {
            "dm": "0b", 
            "hwid": "012b0e6e45", 
            "type": "enter"
            }, 
        "replyToken": "2853f8201bdf4bda99e163479fb051e0", 
        "source": {
            "type": "user", 
            "userId": "U789b69431063e4rfr4f4rfr47cfeb9"
        }, 
        "timestamp": 1558955108398, 
        "type": "beacon"
    }

# Messenger

## Profile

    {
        "first_name":"大由",
        "gender":"male",
        "id":"21248311zzzzzzz96",
        "last_name":"湯",
        "locale":"zh_TW",
        "profile_pic":"https://platform-lookaside.fbsbx.com/platform/profilepic/?psid=rrrrrrrrr8696&width=1024&ext=1532450726&hash=AeQzacmMoYogPegS",
        "timezone":8
    }

## Message Event

### Text

    {
        "mid":"5yJMTWGz5RSl3QR2Ti9WNnnRRULsHJt5QKddb-3VdlkDpyyRns_nU3h6yCdxiQS6pbcarntqoNVReN1Moet0dg",
        "seq":626687,
        "text":"你好"
    }

### Sticker

    {
        "attachments":[
            {
                "payload": {
                    "sticker_id":369239263222822,
                    "url":"https://scontent.xx.fbcdn.net/v/t39.1997-6/851557_369239266556155_759568595_n.png?_nc_cat=0&_nc_ad=z-m&_nc_cid=0&oh=7ad507ccf2fc5ee0771880274673e935&oe=5BDA12DC"
                },
                "type":"image"
            }
        ],
        "mid":"O0CVaIq2EH12Kc_Rmh8bCnnRRULsHJt5QKddb-3VdlmGKt5IdW73_rej-IdnHbQYaZsXWs-CWpjIUusH5nNPhQ",
        "seq":626691,
        "sticker_id":369239263222822
    }

### Image

    {
        "attachments":[
            {
                "payload": {
                    "url":"https://scontent.xx.fbcdn.net/v/t1.15752-9/37597958_1986795468037865_2780148642986590208_n.jpg?_nc_cat=0&_nc_ad=z-m&_nc_cid=0&oh=0b45b86732cfb7fcdb7b62525d11a1cd&oe=5BDC9560"
                },
                "type":"image"
            }
        ],
        "mid":"U3d2uiIQXq5dHclVoMhInXnRRULsHJt5QKddb-3VdllYkPxoB2EbEEVjTsOhIFbgqhm-w5qbG7mvg6VYmSTyOw",
        "seq":626695
    }

### Location

    {
        "attachments":[
            {
                "payload":{
                    "coordinates":{
                        "lat":25.053584447418,
                        "long":121.55250412353
                    }
                },
                "title":"大由 Location",
                "type":"location",
                "url":"https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.bing.com%2Fmaps%2Fdefault.aspx%3Fv%3D2%26pc%3DFACEBK%26mid%3D8100%26where1%3D25.053584447418%252C%2B121.55250412353%26FORM%3DFBKPL1%26mkt%3Den-US&h=AT2c5rZ2ZAp9BC9481ySR8GfRSYqfnp4M6dEmg9EAN9HOEOBJB0BWZ4ALULP8Xr2m8WRjBL5V4TjngC7W-PQ38Qk6quY5LyOPpCUuSaQEDn-8bYZ15QAPxfOq5p1xEvjZ5Ja7Ls4cHyx4go&s=1"
            }
        ],
        "mid":"dSBKoPHbnDUCl4VlA-In7nnRRULsHJt5QKddb-3Vdlnx9uaWifSCI_0pgrJ0HhrKCE21CQM41VN1ucZ5WOOyrg",
        "seq":626699
    }

## Postback Event

    {
        "payload": "SHOWLOC", 
        "title": "顯示位置"
    }
