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
