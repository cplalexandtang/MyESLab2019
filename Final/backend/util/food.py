from linebot.models import TextSendMessage, ImageSendMessage, VideoSendMessage
from linebot.models import AudioSendMessage, LocationSendMessage, StickerSendMessage, TemplateSendMessage
from linebot.models import ButtonsTemplate, ConfirmTemplate, CarouselTemplate, ImageCarouselTemplate
from linebot.models import PostbackTemplateAction, MessageTemplateAction, URITemplateAction, CarouselColumn

import random
import requests
import json
import datetime
import time

URL1 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
URL2 = "https://maps.googleapis.com/maps/api/place/details/json?placeid="
URL3 = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference="
RADIUS = "&radius="
TOKEN = "&key=AIzaSyDWUKKnJbmf1Lgayw2Op35IlZP2SAvlo_M"
language = "&language=zh-TW"

WP = ["王品", "西堤", "陶板屋", "原燒", "聚北海道昆布鍋", "藝奇", "夏慕尼", "品田", "石二鍋", "舒果", "HOT7", "ITA", "莆田", "酷必", "麻佬大", "乍牛", "沐越", "青花驕"]

def get_restaurants(location, radius=350):

	print(URL1+location+RADIUS+str(radius)+"&type=restaurant"+TOKEN+language)
	resp = requests.get(URL1+location+RADIUS+str(radius)+"&type=restaurant"+TOKEN+language)
	places = list()
	resp = json.loads(resp.text)

	for place in resp["results"]:
		if len(place["name"]) > 30:
			continue

		try:
			rating = place["rating"]
		except:
			rating = 0
		try:
			photo_url = place["photos"][0]["photo_reference"]
			photo_auth = place["photos"][0]["html_attributions"]
		except:
			continue
			#photo_url = "NA"
			#photo_auth = "NA"
		if rating >= 3.8:
			places.append({
					"id" : place["place_id"],
					"pic_url" : URL3 + photo_url + TOKEN,
					"attr" : photo_auth,
					"rating" : place["rating"]
				}
			)
	'''
	if "next_page_token" in resp:
		time.sleep(2)
		nextpage = "pagetoken=" + resp["next_page_token"]
		resp2 = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?"+nextpage+TOKEN+language)
		resp2 = json.loads(resp2.text)
		for place in resp2["results"]:
			if len(place["name"]) > 30:
				continue

			skip = False
			for b in BL:
				if b in place["name"]:
					skip = True
					break
			if skip == True:
				continue

			try:
				rating = place["rating"]
			except:
				rating = 0
			try:
				photo_url = place["photos"][0]["photo_reference"]
				photo_auth = place["photos"][0]["html_attributions"]
			except:
				photo_url = "NA"
				photo_auth = "NA"
			if rating >= 3.8:
				places.append({
						"id" : place["place_id"],
						"pic_url" : URL3 + photo_url + TOKEN,
						"attr" : photo_auth,
						"rating" : place["rating"]
					}
				)

		if "next_page_token" in resp2:
			time.sleep(2)
			nextpage = "pagetoken=" + resp2["next_page_token"]
			resp3 = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?"+nextpage+TOKEN+language)
			resp3 = json.loads(resp3.text)
			for place in resp3["results"]:
				if len(place["name"]) > 30:
					continue

				skip = False
				for b in BL:
					if b in place["name"]:
						skip = True
						break
				if skip == True:
					continue

				try:
					rating = place["rating"]
				except:
					rating = 0
				try:
					photo_url = place["photos"][0]["photo_reference"]
					photo_auth = place["photos"][0]["html_attributions"]
				except:
					photo_url = "NA"
					photo_auth = "NA"
				if rating >= 3.8:
					places.append({
							"id" : place["place_id"],
							"pic_url" : URL3 + photo_url + TOKEN,
							"attr" : photo_auth,
							"rating" : place["rating"]
						}
					)
	'''
	random.shuffle(places)

	i = 0
	for idx, place in enumerate(places):
		r = get_restaurants_details(place["id"])
		if "result" not in r:
			continue

		place.update({"name" : r["result"]["name"]})
		place.update({"vicinity" : r["result"]["vicinity"]})
		place.update({"loc" : str(r["result"]["geometry"]["location"]["lat"]) + "," + str(r["result"]["geometry"]["location"]["lng"])})
		try:
			place.update({"website" : r["result"]["website"]})
		except:
			place.update({"website" : "https://www.google.com.tw/search?q=" + r["result"]["name"]})
		try:
			place.update({"phone" : r["result"]["formatted_phone_number"]})
		except:
			place.update({"phone" : "tel:NA"})
		try:
			place.update({"opening_hours" : r["result"]["opening_hours"]["weekday_text"]})
		except:
			place.update({"opening_hours" : "NA"})
		try:
			place.update({"price" : r["result"]["price_level"]})
		except:
			place.update({"price" : "NA"})

		for w in WP:
			if w in place["name"]:
				places[i], places[idx] = places[idx], places[i]
				i += 1

	return places

def get_restaurants_details(id):
	r = requests.get(URL2+id+TOKEN+language)
	r = json.loads(r.text)
	return r

def list_nearby_restaurants(lat, lng, radius=350, ad=True):
	# Get near restaurants
	resp = get_restaurants(str(lat)+","+str(lng), radius=radius)
	
	# Deal with jet lag
	if datetime.datetime.today().hour >= 16:
		today = (datetime.datetime.today().weekday() + 1) % 7
	else:
		today = datetime.datetime.today().weekday()
	
	columns = list()
	
	# Define First/Second class Administration regions
	#firstAdm = ["縣", "市"]
	#secondAdm = ["鄉", "鎮", "市", "區"]
	for r in resp:
		if len(columns) > 7:
			break
		#address = r["vicinity"] if r["vicinity"][2] not in firstAdm else r["vicinity"][3:]
		#address = address if address[2] not in secondAdm else address[3:]
		#address + "\n"
		text =  "評價: " + str(r["rating"]) + "顆星\n"
		try:
			text += "照片來源: " + r["attr"][0].split(">")[1].split("<")[0]
		except:
			text += "照片來源: "
		try:
			op_time = "\n"
			for t in r["opening_hours"]:
				op_time += (t + "\n")
		except:
			op_time = "尚無資料"

		if len(op_time) >= 150:
			op_time = "尚無資料"
		if len(text) >= 30:
			text += "照片來源: "
		
		#requests.post("http://35.197.87.217:5000/api/record_listed_restaurant", json = {"place_id" : r["id"], "name" : r["name"]})

		columns.append(
			CarouselColumn(
				thumbnail_image_url=r["pic_url"],
				title=r["name"],
	            text=text,
	            actions=[
	            	MessageTemplateAction(
						label="營業時間",
						text="Opening|" + op_time
					),
					MessageTemplateAction(
						label="顯示位置",
						text="ImageMap:" + r["loc"] + ":" + r["vicinity"]
					),
	                MessageTemplateAction(
						label="更多資訊",
						text="Location:" + r["id"]
					)
	            ]
	        )
	    )

	columns.append(
		CarouselColumn(
			thumbnail_image_url="https://i.imgur.com/4JTe8Wa.jpg",
			title="查看更多",
	        text="想查看更多地點嗎?小夏可以繼續幫你找美食喔~",
	        actions=[
	        	MessageTemplateAction(
					label="搜尋半徑800公尺",
					text="More2:搜尋半徑800公尺|"+str(lat)+","+str(lng)
				),
	            MessageTemplateAction(
					label="搜尋半徑1600公尺",
					text="More3:搜尋半徑1600公尺|"+str(lat)+","+str(lng)
				),
				MessageTemplateAction(
					label="搜尋半徑3200公尺",
					text="More4:搜尋半徑3200公尺|"+str(lat)+","+str(lng)
				)
	        ]
	    )
	)

	return TemplateSendMessage(
		alt_text='Carousel template',
		template=CarouselTemplate(
				columns = columns
			)
		)

def list_restaurant_details(id):
	resp = get_restaurants_details(id)
	if resp["status"] != "OK":
		return TextSendMessage(text="地點錯誤，請再試一次~")
	else:
		try:
			website = resp["result"]["website"]
		except:
			website = "https://www.google.com/search?q=" + resp["result"]["name"]
		try:
			author = resp["result"]["photos"][0]["html_attributions"][0].split(">")[1].split("<")[0]
		except:
			author = ""
		return TemplateSendMessage(
			alt_text="Buttons template",
			template=ButtonsTemplate(
				thumbnail_image_url=URL3 + resp["result"]["photos"][0]["photo_reference"] + TOKEN,
				title=resp["result"]["name"],
				text="您想更了解麼呢?\n照片來源: " + author,
				actions=[
					MessageTemplateAction(
						label="撥打電話",
						text="tel:" + resp["result"]["formatted_phone_number"].replace(" ", "")
					),
					URITemplateAction(
	                    label="前往網站",
	                    uri=website.replace(" ", "")
	                ),
	                URITemplateAction(
	                    label="探索食記",
	                    uri="https://www.google.com/search?q=" + resp["result"]["name"].replace(" ", "") + "+食記"
	                )
				]
			)
		)

def address_details(lat, lng, adr):
	return LocationSendMessage(
    	title="顯示位置",
    	address=adr,
    	latitude=lat,
    	longitude=lng
	)

def add_bookmark(user_id, place_id):
	resp = requests.post("http://35.197.87.217:5000/api/record_bookmark/" + user_id, json={"place_id" : place_id})
	print("------> rsp: ", resp.text)
	if (json.loads(resp.text))["status"] == "Exists":
		return 1
	elif (json.loads(resp.text))["status"] != "OK":
		return -1
	return 0

def list_bookmarks(user_id):
	resp = requests.get("http://35.197.87.217:5000/api/get_bookmark/" + user_id)
	resp = json.loads(resp.text)["result"]

	columns = list()
	# Deal with jet lag
	if datetime.datetime.today().hour >= 16:
		today = (datetime.datetime.today().weekday() + 1) % 7
	else:
		today = datetime.datetime.today().weekday()

	for r in resp:
		if r == "0":
			continue

		data = get_restaurants_details(r)["result"]

		try:
			opening = data["opening_hours"]["weekday_text"][today]
		except:
			opening = ""
		try:
			author = data["photos"][0]["html_attributions"][0].split(">")[1].split("<")[0]
		except:
			author = ""
		try:
			rating = str(data["rating"])
		except:
			rating = ""
		try:
			vicinity = data["vicinity"]
		except:
			vicinity = "地址"

		text =  "評價: " + rating + "顆星\n"
		text += "照片來源: " + author

		columns.append(
			CarouselColumn(
				thumbnail_image_url=URL3 + data["photos"][0]["photo_reference"] + TOKEN,
				title=data["name"],
	            text=text,
	            actions=[
	            	MessageTemplateAction(
						label="營業時間",
						text="Opening|" + opening
					),
					MessageTemplateAction(
						label="顯示位置",
						text="ImageMap:" + str(data["geometry"]["location"]["lat"]) + "," + str(data["geometry"]["location"]["lng"]) + ":" + vicinity
					),
	                MessageTemplateAction(
						label="更多資訊",
						text="Location:" + data["place_id"]
					)
	            ]
	        )
		)

	if len(columns) != 0:
		return TemplateSendMessage(
			alt_text='Carousel template',
			template=CarouselTemplate(
				columns = columns
			)
		)
	else:
		return TextSendMessage(text="你還沒新增任何東西喔~")

def list_bookmarks_to_delete(user_id):
	resp = requests.get("http://35.197.87.217:5000/api/get_bookmark/" + user_id)
	resp = json.loads(resp.text)["result"]

	columns = list()
	# Deal with jet lag
	if datetime.datetime.today().hour >= 16:
		today = (datetime.datetime.today().weekday() + 1) % 7
	else:
		today = datetime.datetime.today().weekday()

	for r in resp:
		if r == "0":
			continue

		data = get_restaurants_details(r)["result"]

		try:
			opening = data["opening_hours"]["weekday_text"][today]
		except:
			opening = ""
		try:
			author = data["photos"][0]["html_attributions"][0].split(">")[1].split("<")[0]
		except:
			author = ""

		text =  "評價: " + str(data["rating"]) + "顆星\n"
		text += "照片來源: " + author

		columns.append(
			CarouselColumn(
				thumbnail_image_url=URL3 + data["photos"][0]["photo_reference"] + TOKEN,
				title=data["name"],
	            text=text,
	            actions=[
	            	MessageTemplateAction(
						label="刪除",
						text="ConfirmDeleteBookmark:" + r
					)
	            ]
	        )
		)

	if len(columns) != 0:
		return TemplateSendMessage(
			alt_text='Carousel template',
			template=CarouselTemplate(
				columns = columns
			)
		)
	else:
		return TextSendMessage(text="你還沒新增任何東西喔~")

def delete_bookmark(user_id, place_id):
	resp = requests.post("http://35.197.87.217:5000/api/delete_bookmark/" + user_id, json = {"place_id" : place_id})
	resp = json.loads(resp.text)
	if resp["status"] == "OK":
		return TextSendMessage(text="刪除成功!")
	else:
		return TextSendMessage(text="地點錯誤，請再試一次~")

