import requests
import json

# legge una  barzelletta chcuck
def getWitz(g):
    # PROCEDURA MAIN recupera un witz
    if g == 'any':
        url = 'http://api.icndb.com/jokes/random'
        intro = 'Te ne racconto una a caso...\n'
    else:
        url = 'http://api.icndb.com/jokes/random?limitTo=[' + g +']'
        intro = 'Te ne racconto una  ' + g + ". \n"
        print(url)

    r = requests.get(url)

    if r.status_code != 200:
        pass
        witz = '...'
        intro = 'Non ne ho una da raccontare...'
    else:
        full_json = r.text
        full = json.loads(full_json)
        witz = (full['value']['joke'])

    # togli i caratteri escape
    witz = html_decode(witz)
    print ('W:', witz)

    witz = intro + witz
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
