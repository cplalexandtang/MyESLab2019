import sys
sys.path.append("..")

from config import googleConfig
import requests
import json
import random

def getPlaces(location, **kwargs):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    payload = {
        "key" : googleConfig.get("token"),
        "location" : location,
        "radius" : "350",
        "type" : "restaurant",
        "language" : "zh-TW"
    }
    payload.update(kwargs) 

    result = requests.get(url, params = payload)
    print("Radar Search URL: " + result.url)
    result = json.loads(result.text).get("results")
    
    return getDetails(result)

def getDetails(places):
    details = list()
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    photo = "https://maps.googleapis.com/maps/api/place/photo"

    random.shuffle(places)
    places = places[:15]

    for place in places:
        if len(details) > 9: break

        payload = {
            "key" : googleConfig.get("token"),
            "placeid" : place.get("place_id"),
            "language" : "zh-TW"
        }
        detail = requests.get(url, params = payload)
        uri = detail.url
        print("Detail Search URL: " + uri)
        
        detail = json.loads(detail.text).get("result")
        if not detail : break 

        if detail.get("photos"):
            source = detail.get("photos")[0].get("html_attributions")[0].split(">")[1].split("<")[0]
            photourl = requests.get(photo, params = {
                "key" : googleConfig.get("token"),
                "photoreference" : detail.get("photos")[0].get("photo_reference"),
                "maxwidth" : "1600"
            }).url
        else: continue

        if detail.get("rating"):
            pass
        else: continue
        
        if detail.get("rating") >= 3.8:
            details.append({
                "name" : detail.get("name"),
                "rating" : detail.get("rating"),
                "address" : detail.get("formatted_address"),
                "phone" : detail.get("formatted_phone_number"),
                "opening" : detail.get("opening_hours"),
                "photo" : {
                    "source" : source,
                    "url" : photourl
                },
                "url" : uri,
                "website" : detail.get("website"),
                "location" : str(detail.get("geometry").get("location").get("lat")) + "," + str(detail.get("geometry").get("location").get("lng"))
            })
    return details