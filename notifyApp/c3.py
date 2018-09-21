

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '3f9279ffb28e4321bce5c3e9b4b0b434',
}

params = urllib.parse.urlencode({
    # Request parameters
    'q': 'cats',
    'count': '10',
    'offset': '0',
    'mkt': 'en-us',
    'safeSearch': 'Moderate',
})



try:
    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
    conn.request("GET", "/bing/v7.0/images/search?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################

