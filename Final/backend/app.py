# Unified Chatbot Interface (UCI)

from flask import Flask, request, abort, render_template, jsonify
#from messenger import page
from line import handler

import config

app = Flask(__name__)

# Messenger
'''@app.route("/webhook", methods=["GET"])
def validate():
    secret = config.messengerConfig.get("secret")
    if request.args.get("hub.mode", "") == "subscribe" and request.args.get("hub.verify_token", "") == secret:
        print("Validating webhook")
        return request.args.get("hub.challenge", "")
    else:
        return "Failed validation. Make sure the validation tokens match."'''

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        page.handle_webhook(request.get_data(as_text=True))
    except Exception as e:
        print(e)
        abort(400)
    return "OK"

# Line
@app.route("/callback", methods=["POST"])
def callback():
    try:
        handler.handle(request.get_data(as_text=True), request.headers["X-Line-Signature"])
    except Exception as e:
        if request.headers.get("X-Line-Signature"):
            return "OK"
        print(e)
        abort(400)
    return "OK"

# API
@app.route("/status")
def status():
    import api.number as num

    queue = num.UserQueue()
    res = queue.waitingList()

    print(res)
    return jsonify({
        "waiting_list" : res
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9487, debug=True)
