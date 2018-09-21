# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import speech_recognition as sr  
import numpy as np
import httplib, urllib, base64, json
from django.http import HttpResponse
import datetime
import json
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
from django.views.decorators.csrf import csrf_exempt
import http.client, json
import urllib2

def BingWebSearch(search,subscriptionKey):
	host = "api.cognitive.microsoft.com"
	path = "/bing/v7.0/search"
	headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
	conn = http.client.HTTPSConnection(host)
	# query = urllib.parse.quote(search)
	conn.request("GET", path + "?q=" + search, headers=headers)
	response = conn.getresponse()
	headers = [k + ": " + v for (k, v) in response.getheaders() if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
	return headers, response.read().decode("utf8")



@csrf_exempt

def imagesearch(request):
	headers = {
	# Request headers
	'Ocp-Apim-Subscription-Key': '3f9279ffb28e4321bce5c3e9b4b0b434',
	}

	query = request.POST["imquery"]
	params = "q=" + query + "&count=5&offset=0&mkt=en-us&safeSearch=Moderate"

	try:
		conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
		conn.request("GET", "/bing/v7.0/images/search?%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()

		result =  json.loads(data)
		ans =""
		for a in result["value"]:
			ans += "<b>" + a["name"] + "</b><br>" + "<img style='height:100px' src='" + a["thumbnailUrl"]+ "'/>" + "<br><br>"
		conn.close()
		# return HttpResponse(ans)
		return ans;

	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))


def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context_dict)
	result = StringIO.StringIO()

	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
	    return HttpResponse(result.getvalue(), content_type='application/pdf')
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

@csrf_exempt
def search(request):

	subscriptionKey = "3f9279ffb28e4321bce5c3e9b4b0b434"
	ans =""
	term = request.POST["query"]
	if len(subscriptionKey) == 32:
		headers, result = BingWebSearch(term,subscriptionKey)
	result =  json.loads(result)
	for a  in result["webPages"]["value"]:
			ans +=  "\n" + a["name"]+ "\n" + a["snippet"] + "\n\n"
	
	return ans;


@csrf_exempt
def home(request):

	if request.method == 'GET':
		return render(request , "index.html")
	else:
		already = request.POST["already"]
		qt = request.POST["qt"]
		if qt=="i2t":
			subscription_key = 'ea88cf5209ca4d95b6628a83df5c1d29'
			uri_base = 'https://westcentralus.api.cognitive.microsoft.com?'

			url = request.POST['imageurl']
			# return HttpResponse(url)
			headers = {
			    # Request headers.
			    'Content-Type': 'application/json',
			    'Ocp-Apim-Subscription-Key': 'ea88cf5209ca4d95b6628a83df5c1d29',
			}

			params = urllib.urlencode({
			    # Request parameters. All of them are optional.
			    'language':'unk',
			    'detectOrientation':'true'
			    
			})

			# The URL of a JPEG image to analyze.
			# body = "{'url':'https://about.canva.com/wp-content/uploads/sites/3/2017/02/congratulations_-banner.png'}"
			body = "{'url': '" + url + " '}"



			# Execute the REST API call and get the response.
			conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
			conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
			response = conn.getresponse()
			data = response.read()

			# 'data' contains the JSON data. The following formats the JSON data for display.
			parsed = json.loads(data)

			conn.close()
			ans =""

			for a in parsed["regions"]:
				for b in a["lines"]:
					for c in b["words"]:
						try:
							ans += c["text"].encode("ASCII")  + "  "
						except:
							continue
			# return render_to_pdf("pdf.html" , )
			
			return render(request , "index.html"  , {'data': already + " " + ans })
		if qt=="search":
			ans = search(request);
			return render(request , "index.html"  , {'data': already + " " + ans }) 
		if qt=="imsearch":
			ans = imagesearch(request)
			return HttpResponse(ans)
			# return render(request , "index.html"  , {'idata':  ans }) 


@csrf_exempt
def getTextFromImage(request):
	try:
		ans = request.POST["data"].encode("ASCII")
	except:
		pass
	return render_to_pdf("pdf.html" , {'languague':ans })


def getTextFromSound(request):

	f=file('python.mp3', 'w')
	url=urllib2.urlopen("http://mp3.streampower.be/radio1-high.mp3")
	audio = 0
	while True:
	    audio += url.read(1024)


	# r = sr.Recognizer()                                                                                   
	# with sr.Microphone() as source:                                                                       
	#     print("Speak:")                                                                                   
	#     audio = r.listen(source)   
	 
	try:
	    print("You said " + r.recognize_google(audio))
	except sr.UnknownValueError:
	    print("Could not understand audio")
	except sr.RequestError as e:
	    print("Could not request results; {0}".format(e))

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)