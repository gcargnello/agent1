#!/usr/bin/env python
import json
import os
import requests
import random, time

from  routines import getWitz, getCats, getTicketsbyCustomerStatusPrio, getTicketbyID, putTicket
from  routines import sendEvent, getAlarm1, sendSlack

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify

global machineAlert
global issue_description
machineAlert = '...'

# Flask app should start in global layout..
app = Flask(__name__)


@app.route('/')
def index():
    return "<h2>DialogFlow/Recast.Ai Agent<h2>"

@app.route('/webhook', methods=['POST'])
def webhook():
    global machineAlert

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

@app.route('/alert', methods=['POST'])
def alert():
    global machineAlert
    req = request.get_json(silent=True, force=True)

#   Stampa il JSON di richiesta
    print("Request:")
    print(json.dumps(req, indent=4))

#    sId = '1c081760-23bf-4ef2-845f-c8d45cbc1514'
    machineAlert = req.get("text")
    sId = '@FD4DIbot'
#    r = sendEvent(sId)
    r = machineAlert

    return r

@app.route('/slack', methods=['POST'])
def slack():
    global machineAlert
    req = request.get_json(silent=True, force=True)

#   Stampa il JSON di richiesta
    print("Request:")
    print(json.dumps(req, indent=4))

    machineAlert = req.get("text")
    r = sendSlack(machineAlert)

    return r


@app.route('/recast', methods=['POST'])
def recast():

    global issue_description
    r1 = request.get_json(silent=True, force=True)
    req = json.loads(request.get_data())

    print("Request:")
    print(json.dumps(r1, indent=4))

    s = req['nlp']['source']

    reply = '.'
    issue_description = ''
    image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQav9X1mzK7qkfDWo1_ZcODCT_hFva2Uw6zt5j2SqbyCSU8AlhI'

#   print(json.loads(request.get_data()))
    return jsonify(
        status=200,
        replies=
        [
            {
                'type': 'picture',
                'content': image
            }
        ],
        conversation={
            'memory': {'key': 'value'}
        }
    )

    return 0

@app.route('/save_description', methods=['POST'])
def save_description():

    global issue_description
    req = json.loads(request.get_data())

    s = req['nlp']['source']
    issue_description = s
    print('save_description')
    print(issue_description)
    reply = 'ok'

    #   print(json.loads(request.get_data()))
    return jsonify(
        status=200,
        replies=
        [
            {
                'type': 'text',
                'content': reply
            }
        ]
        }
    )

    return


@app.route('/get_description', methods=['POST'])
def get_description():

    global issue_description
    r1 = request.get_json(silent=True, force=True)
    req = json.loads(request.get_data())

    print("Request:")
    print(json.dumps(r1, indent=4))

    reply = 'Your said that ' + issue_description


#   print(json.loads(request.get_data()))
    return jsonify(
        status=200,
        replies=
        [
            {
                'type': 'text',
                'content': reply
            }

        ]
    )

    return 0


@app.route('/create_notification', methods=['POST'])
def create_notification():

    r1 = request.get_json(silent=True, force=True)
    req = json.loads(request.get_data())

    print("Request:")
    print(json.dumps(r1, indent=4))


    s = req['nlp']['source']

    time.sleep(3)
    notification_id = str(random.randint(5006000,5007999))
    reply = 'Notification '+ notification_id + ' created'


#   print(json.loads(request.get_data()))
    return jsonify(
        status=200,
        replies=
        [
            {
                'type': 'text',
                'content': reply
            }
        ],
        conversation={
            'memory': {'notification_id': notification_id}
        }
    )

    return 0


def makeWebhookResult(req):
#   controllo della azione determinata dalla richiesta API.AI.
    global machineAlert
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

    elif action == 'yAlarm1':

        return {"followupEvent": {"name": "E_Machine_Alert2", "data": {}}}

    elif action == 'yAlarm2':

        speech = machineAlert
#        if speech == '...':
#            return { "followupEvent": {"name": "E_Machine_Alert2","data": {}}}

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
        "source": "Chatbot Demo FD4DI"
        }

# TEST crea ticket
@app.route('/tkput', methods=['POST'])
def tkput():

    # C4C demo
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
        tkn = req.headers.get('x-csrf-token')
#        tkn = 'jP5tMqxSSkbRB9M-FNp7XQ=='
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

    return "<h2>Ticket Create<h2>"

# Statement standard Flask per avviamento in localhost
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
#    print ("Starting app on port %d" % port)
#    app.run(debug=True, port=port, host='0.0.0.0')
    app.run()
