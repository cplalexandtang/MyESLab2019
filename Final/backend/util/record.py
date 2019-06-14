import requests
import json

URL = "http://35.197.87.217:5000/api/"

def get_status(user_id):
	resp = requests.get(URL + "get_status/" + user_id)
	resp = json.loads(resp.text)
	return resp["result"]

def record_status(user_id, status):
	data = {
		"game_status" : status[0],
		"visited" : status[1],
		"coupon_1_num" : status[2],
		"coupon_2_num" : status[3],
		"coupon_3_num" : status[4],
		"coupon_4_num" : status[5],
		"coupon_5_num" : status[6],
		"egg_status" : status[7]
	}
	requests.post(URL + "record_status/" + user_id, json = data)

def record_message(profile, msg):
	data = {
		"user_id" : profile.user_id,
		"name" : profile.display_name,
		"pic_url" : profile.picture_url,
		"msg" : msg
	}
	requests.post(URL + "record_message/" + profile.user_id, json = data)

#if __name__ == "__main__":
	#print(get_status("cplalexandtang"))