#!/usr/bin/env python
import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout.
app = Flask(__name__)


@app.route('/')
def index():
    return "<h2>API AI agent<h2>"

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

#    speech = "Te ne racconto una di genere " + genere
    speech = getWitz()


    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "Agent1"
    }

# legge una  barzelletta chcuck
def getWitz():
    # PROCEDURA MAIN recupera un witz a caso
    url = 'http://api.icndb.com/jokes/random'

    r = requests.get(url)

    if r.status_code != 200:
        pass
        witz = 'Non ne ho una da raccontare...'
    else:
        full_json = r.text
        full = json.loads(full_json)
        witz = (full['value']['joke'])

    # togli i cartteri escape
    witz = html_decode(witz)
    print ('W:', witz)

    return witz

# escape decode
def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

# Statement standard Flask per avviamento in localhost
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
#    app.run(debug=True, port=port, host='0.0.0.0')
    app.run()
