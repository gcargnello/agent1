import requests
import json

global machineAlert

# legge una  barzelletta chcuck
def getWitz(usr,g):
    # PROCEDURA MAIN recupera un witz
    if g == 'any':
        url = 'http://api.icndb.com/jokes/random'
        intro = 'Te ne racconto una a caso...\n'
    else:
        url = 'http://api.icndb.com/jokes/random?limitTo=[' + g +']'
        intro = 'OK '+ usr + 'Te ne racconto una  ' + g + ". \n"
        print(url)

    r = requests.get(url)

    if r.status_code != 200:
        pass
        witz = '....'
        intro = 'Sorry ' + usr + 'Non ne ho una da raccontare....'
    else:
        full_json = r.text
        full = json.loads(full_json)
        witz = (full['value']['joke'])

    # togli i caratteri escape
    witz = html_decode(witz)
    print ('W:', witz)

    witz = intro + witz
    return witz

# legge una massima sui gatti
def getCats(usr):
    #
    url = 'http://catfacts-api.appspot.com/api/facts'
    intro = usr + ', se ti piacciono i gatti senti questa...\n'

    print(url)
    r = requests.get(url)

    if r.status_code != 200:
        pass
        fact = '...'
        intro = 'mi dispiace ' + usr + 'mmm adesso non mi viene in mente niente...'
    else:
        full_json = r.text
        full = json.loads(full_json)
        fact = full['facts'][0]


    # togli i caratteri escape
    fact = html_decode(fact)
    print ('G:', fact)

    fact = intro + fact
    return fact


def sendEvent(sId):
    # lancia un evento DialogFlow

    hdr = {
        'Authorization': 'Bearer 569c091c1458408a83e99c04e79888f7'
        }

    url = "https://api.dialogflow.com/v1//query?v=20170712&e=E_Machine_Alert1&sessionId="
    sessionID = sId
    url = url + sessionID + "&lang=en"


    r = requests.get(url, headers=hdr)

    if r.status_code != 200:
        pass
        r = 'KO'
    else:
        full_json = r.text
        full = json.loads(full_json)
        r = (full['result']['resolvedQuery'])

    return r

def getAlarm1():
    global machineAlert
    # recupera il msg di allarme

    r = machineAlert

    return r

# legge
def getTicketsbyCustomerStatusPrio(Id,Pr,St,Nu):
    #
    hdr = {'Authorization': 'Basic c2VydmljZWFkbWluMDE6ZXhwcml2aWE='}
    url = 'https://my307032.crm.ondemand.com/sap/c4c/odata/v1/c4codata/ServiceRequestCollection/'
    intro = ''

 #   stabilisce default per parametri indefiniti
    if Pr == '':
        Pr= '*'
    if St == '':
        St= '*'
    if Nu == '':
        Nu = 10

#   build query
    q = '?'
    order = '$orderby=ID desc&'
    top = q + order + '$inlinecount=allpages&$skip=0&$top=' + str(Nu) + '&'
    query = '$filter=CustomerID eq ' + '\'' + Id + '\''
    query = query + ' and ServicePriorityCode eq ' + '\'' + Pr + '\''
    query = query + ' and ServiceRequestLifeCycleStatusCode eq ' + '\'' + St + '\''
    # query = '$count'
    frm = '&$format=json'


    url = url + top + query + frm
    print(url)
    r = requests.get(url, headers=hdr)

    if r.status_code != 200:
        pass
        fact = '...'
        intro = 'mi dispiace in questo momento non riesco a rispondere...'
        print (intro)
    else:
        full_json = r.text
        full = json.loads(full_json)
        a1 = full['d']
        cn = a1['__count']
        a2 = a1['results']

    a3 = ''
    for t in a2:
        a3 = a3 + t['ID'] + ' ' + t['Name']['content'] + '-' + t['ServicePriorityCodeText'] #+ t['ServicePriorityCode']
        a3 = a3 + '-' + t['CustomerID'] + ':' + t['Customer']
#        a3 = a3 + '-uuid:' + t['ObjectID'] + '-' + t['ServiceRequestLifeCycleStatusCodeText']
        a3 = a3 + '-' + t['ServiceRequestLifeCycleStatusCodeText']
#        a3 = a3 + ' w:' + t['ItemListServiceRequestExecutionLifeCycleStatusCodeText']
        a3 = a3 + '\n'

#    print (a3)

    if a3 == '':  # non ci sono ticket
        a4 = 'Mi dispiace non ho trovato nessun ticket per i criteri indicati.'
    elif len(a2) >= cn:     # ci sono e li ho elencati tutti
        a4 = 'Ho trovato ' + str(cn) + ' tickets. Eccoli:\n' + a3
    else:
        a4 = 'Ho trovato ' + str(cn)  + ' tickets. Ecco gli ultimi ' + str(len(a2)) + ':\n' + a3

    # togli i caratteri escape
#    fact = html_decode(fact)
    print ('C4C:', a4)

    return a4

##################################################################
def getTicketbyID(Id):
    #
    hdr = {'Authorization': 'Basic c2VydmljZWFkbWluMDE6ZXhwcml2aWE='}
    url = 'https://my307032.crm.ondemand.com/sap/c4c/odata/v1/c4codata/ServiceRequestCollection/'
    intro = ''

#   build query
    q = '?'
#    order = '$orderby=ID desc&'
    query = q + '$filter=ID eq ' + '\'' + Id + '\''
    frm = '&$format=json'


    url = url + query + frm
    print(url)
    r = requests.get(url, headers=hdr)

    if r.status_code != 200:
        pass
        fact = '...'
        intro = 'mi dispiace in questo momento non riesco a rispondere...'
        print (intro)
    else:
        full_json = r.text
        full = json.loads(full_json)
        print (full)
        a1 = full['d']
        a2 = a1['results']

    a3 = ''
    for t in a2:
        a3 = a3 + t['ID'] + ' ' + t['Name']['content'] + '-' + t['ServicePriorityCodeText'] #+ t['ServicePriorityCode']
        a3 = a3 + '-' + t['CustomerID'] + ':' + t['Customer']
#        a3 = a3 + '-uuid:' + t['ObjectID'] + '-' + t['ServiceRequestLifeCycleStatusCodeText']
        a3 = a3 + '-' + t['ServiceRequestLifeCycleStatusCodeText']
#        a3 = a3 + ' w:' + t['ItemListServiceRequestExecutionLifeCycleStatusCodeText']
        a3 = a3 + '\n'

#       la descrizione
        d1 = t['ServiceRequestDescription']['__deferred']['uri']
        url_d = d1 + '?' + frm
        rd = requests.get(url_d, headers=hdr)
        if r.status_code != 200:
           pass
           fact = '...'
           intro = 'Problema oon la descrizione...'
           print (intro)
        else:
          full_json = rd.text
          full = json.loads(full_json)
          try:
             d2 = full['d']['results'][0]['Text']
             a3 = a3 + d2 + '\''
          except:
              pass



    #    print (a3)

    if a3 == '':  # non ci sono ticket
        a4 = 'Mi dispiace non ho trovato il ticket ' + Id
    else:
        a4 = a3

    # togli i caratteri escape
#    fact = html_decode(fact)
    print ('C4C:', a4)

    return a4


##################################################################
def putTicket(Id,Pr,Nm,Ds):
    # C4C demo Exprivia

#   url per fetch del token
    url_c4c = 'https://my307032.crm.ondemand.com/sap/c4c/odata/v1/c4codata/'
    hdr = {'Authorization': 'Basic c2VydmljZWFkbWluMDE6ZXhwcml2aWE=', 'x-csrf-token': 'fetch'}

    # leggiamo il token
    req = requests.get(url_c4c, headers=hdr)
    if req.status_code != 200:
        print('Impossibile leggere il token', req.status_code)
        tkn = ''
    else:
        tkn = req.headers.get('x-csrf-token')
        print ('TOKEN:', tkn)
#    tkn = 'VocREGyshjlDUllmgGw-qw=='

    # adesso creiamo un ticket di prova
    headers = {
                'Authorization': 'Basic c2VydmljZWFkbWluMDE6ZXhwcml2aWE=',
                'Content-Type': 'application/json',
                'x-csrf-token': tkn,
                'Accept': 'application/json'
               }

#    print('HDR:', headers)

    # prepariamo i dati del ticket

    payload = {
        "ProcessingTypeCode": "SRRQ",
        "DataOriginTypeCode": "4",
        "CustomerID": Id,
        "SerialID": "IOT12345",
        "ServicePriorityCode": Pr,
        "Name": {
            "__metadata": {
                "type": "c4codata.EXTENDED_Name"
            },
            "languageCode": "I",
            "content": Nm
        }
    }

    payload = {
	"ProcessingTypeCode": "SRRQ",
    "DataOriginTypeCode": "4",
    "CustomerID" : "1001000",
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
                "content": "PYTHON-New Ticket Created heroku"
              }
}

# URL dei ticket
    url_c4c = 'https://my307032.crm.ondemand.com/sap/c4c/odata/v1/c4codata/ServiceRequestCollection/'
    # posta richiesta creazione ticket
    req = requests.post(url_c4c,
                        headers=headers,
                        data=json.dumps(payload),
                        )

    print (json.dumps(payload))
    if req.status_code != 200:
        print('Errore di connessione a C4C', req.status_code, ":", req.content)
        print(req.headers.get('x-csrf-token'))
    else:
        print(req.url)


    return(req.content)

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
