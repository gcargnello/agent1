#!/usr/bin/env python

import urllib
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
    if req.get("result").get("action") != "yGetWitz":
        return {}

    result = req.get("result")
    parameters = result.get("parameters")
    genere = parameters.get("genere")

#   cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "Te ne racconto una di genere " + genere
#   speech = "Ecco la risposta!"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "Agent1"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

#   app.run(debug=True, port=port, host='0.0.0.0')
    app.run()