import requests
import json

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
        witz = '...'
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


# legge una massima sui gatti
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

    print (a3)

    a4 = 'Ho trovato ' + str(cn)  + ' tickets. Ecco gli ultimi ' + str(len(a2)) + ':\n' + a3

    # togli i caratteri escape
#    fact = html_decode(fact)
    print ('C4C:', a4)

    return a4


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
