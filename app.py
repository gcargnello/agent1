#!/usr/bin/env python
import json
import os
import requests
from  routines import getWitz, getCats, getTicketsbyCustomerStatusPrio, getTicketbyID, putTicket

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
#   controllo della azione determinata dalla richiesta API.AI.
    action = req.get("result").get("action")
#    print ('ACTION:',action)

    result = req.get("result")
    parameters = result.get("parameters")


#   Gestisce le diverse azioni di API.AI
    if action == "yGetWitz":
        genere = parameters.get("genere")
        user = parameters.get("user")
        speech = getWitz(user,genere) # legge un witz

    elif action == "yStop": # ci fermiamo

        speech = 'OK per oggi basta!'

    elif action == 'yCats': # legge una sui gatti
        user = parameters.get("user")
        speech = getCats(user)
#   azioni C4C
    elif action == 'yGetTkbyCust':
        CustomerID = parameters.get("CustomerID")
        Priority = parameters.get("Priority")
        Status = parameters.get("Status")
        nmax = parameters.get("nmax")

        speech = getTicketsbyCustomerStatusPrio(CustomerID,Priority,Status,nmax)
    elif action == 'yGetTkbyID':
        TicketID = parameters.get("TicketID")

        speech = getTicketbyID(TicketID)

    elif action == 'yPutTicket':

        CustomerID = '10005'
        Priority = '2'
        Name = 'Phyton Ticket!'
        Description = 'lorem ipsum'

        speech = putTicket(CustomerID,Priority,Name,Description)
    else:
        return {}


#   chiude con la restituzione della risposta

    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {

                },
        # "contextOut": [],
        "source": "C4C Demo"
    }


# Statement standard Flask per avviamento in localhost
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
#    print ("Starting app on port %d" % port)
#    app.run(debug=True, port=port, host='0.0.0.0')
    app.run()
