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

# TEST crea ticket
@app.route('/tkput', methods=['POST'])
def tkput():

    # C4C demo Exprivia
    url_c4c = 'https://my307032.crm.ondemand.com/sap/c4c/odata/v1/c4codata/ServiceRequestCollection'
    # hdr = {'Authorization': 'Basic c2VydmljZWFkbWluMDE6ZXhwcml2aWE=','x-csrf-token':'fetch'}
    hdr = {
        'Authorization': 'Basic c2VydmljZWFkbWluMDE6ZXhwcml2aWE=',
        'Content-Type': 'application/json',
        'cache-control': 'no-cache',
        'x-csrf-token': 'fetch',
        'Accept': 'application/json'
    }

    # leggiamo il token
    req = requests.get(url_c4c, headers=hdr)
    if req.status_code != 200:
        print('Impossibile leggere il token', req.status_code)
        tkn = ''
    else:
        #    print ('RH:',req.headers)
        tkn = str(req.headers.get('x-csrf-token'))
        #    tkn = 'jP5tMqxSSkbRB9M-FNp7XQ=='
        print ('TOKEN:', tkn)

    # adesso creiamo un ticket di prova
    headers = {
        'Authorization': 'Basic c2VydmljZWFkbWluMDE6ZXhwcml2aWE=',
        'Content-Type': 'application/json',
        'cache-control': 'no-cache',
        'x-csrf-token': tkn,
        'Accept': 'application/json'
    }

    print('HDR:', headers)

    # prepariamo i dati del ticket
    payload = {
        "ProcessingTypeCode": "SRRQ",
        "DataOriginTypeCode": "4",
        "CustomerID": "1001000",
        "ProductID": "IOT00001",
        "SerialID": "IOT12345",
        "ServicePriorityCode": "1",
        "ServiceIssueCategoryID": "OS",
        "IncidentServiceIssueCategoryID": "OS-OS",
        "Name": {
            "__metadata": {
                "type": "c4codata.EXTENDED_Name"
            },
            "languageCode": "I",
            "content": "PYTHON-New Ticket Created"
        }
    }

    url_c4c = 'https://my307032.crm.ondemand.com/sap/c4c/odata/v1/c4codata/ServiceRequestCollection'
    # posta richiesta creazione ticket
    req = requests.post(url_c4c,
                        data=json.dumps(payload),
                        headers=headers
                        )

    if req.status_code != 200:
        print('Errore di connessione a C4C', req.status_code, ":", req.content)
        print(req.headers.get('x-csrf-token'))
    else:
        print(req.url)

    return req.status_code

# Statement standard Flask per avviamento in localhost
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
#    print ("Starting app on port %d" % port)
#    app.run(debug=True, port=port, host='0.0.0.0')
    app.run()
