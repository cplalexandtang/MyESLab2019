# Unified Chatbot Interface (UCI)

from flask import Flask, request, abort, render_template, jsonify
from flask_cors import CORS, cross_origin
#from messenger import page
from line import handler, push_message

import config

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Messenger
'''@app.route("/webhook", methods=["GET"])
def validate():
    secret = config.messengerConfig.get("secret")
    if request.args.get("hub.mode", "") == "subscribe" and request.args.get("hub.verify_token", "") == secret:
        print("Validating webhook")
        return request.args.get("hub.challenge", "")
    else:
        return "Failed validation. Make sure the validation tokens match."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        page.handle_webhook(request.get_data(as_text=True))
    except Exception as e:
        print(e)
        abort(400)
    return "OK"'''

# Line
@app.route("/callback", methods=["POST"])
def callback():
    try:
        handler.handle(request.get_data(as_text=True), request.headers["X-Line-Signature"])
    except:
        '''if request.headers.get("X-Line-Signature"):
            return "OK"
        print(e)
        abort(400)'''
        pass
    return "OK"

# API
import api.number as num

@app.route("/status")
@cross_origin()
def status():
    queue = num.UserQueue()
    res = queue.waitingList()

    return jsonify({
        "waiting_list" : res
    })

@app.route("/call/<number>")
@cross_origin()
def call(number):
    queue = num.UserQueue()
    id = queue.getId(number)
    push_message(id, text="輪到您了! 請盡速前來")

    return "OK"

@app.route("/delete/<number>", methods=["DELETE"])
@cross_origin()
def delete(number):
    queue = num.UserQueue()
    queue.pop(number = number)
    push_message(id, text="您的號碼已被取消，請重新取號")

    return jsonify({
        "status" : "OK"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9487, debug=True)
