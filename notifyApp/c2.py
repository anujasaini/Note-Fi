# -*- coding: utf-8 -*-

import http.client, json
import urllib.parse
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "cacfe72b95974aafa2f2f9390ce90ae7"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/image"

term = "Microsoft Cognitive Services"

def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

if len(subscriptionKey) == 32:

    print('Searching the Web for: ', term)

    headers, result = BingWebSearch(term)
    print("\nRelevant HTTP Headers:\n")
    print("\n".join(headers))
    print("\nJSON Response:\n")
    print(json.dumps(json.loads(result), indent=4))

else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")