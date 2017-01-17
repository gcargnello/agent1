#!/usr/bin/env python
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout.
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

#   Stampa il JSON di richiesta
    print("Request:")
    print(json.dumps(req, indent=4))

#   Determina la risposta
    res = makeWebhookResult(req)
    print('Risposta:',res)

#   Stampa la risposta
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
#   controllo della azione determinata dalla richiesta API.AI
    yaction = req.get("result").get("action")
    if yaction != "yGetWitz":
        return {}

    result = req.get("result")
    parameters = result.get("parameters")
    genere = parameters.get("genere")

    speech = "Te ne racconto una di genere " + genere

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "Agent1"
    }

# Statement standard Flask per avviamento in localhost
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
#    app.run(debug=True, port=port, host='0.0.0.0')

    app.run()
