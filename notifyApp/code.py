import numpy as np
# import cv2
import httplib, urllib, base64, json

subscription_key = 'ea88cf5209ca4d95b6628a83df5c1d29'
uri_base = 'https://westcentralus.api.cognitive.microsoft.com?'

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
body = "{'url':'https://about.canva.com/wp-content/uploads/sites/3/2017/02/congratulations_-banner.png'}"



try:
	# Execute the REST API call and get the response.
	conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
	response = conn.getresponse()
	data = response.read()

	# 'data' contains the JSON data. The following formats the JSON data for display.
	parsed = json.loads(data)
	print ("Response:")
	print (json.dumps(parsed, sort_keys=True, indent=2))
	conn.close()

except Exception as e:
	print('Error:')
	print(e) 
# cap = cv2.VideoCapture(0)
# while(True):
# 	ret, frame = cap.read()

# 	# to convert the frame colorspace 
# 	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	cv2.imshow('frame',frame)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		try:
# 			# Execute the REST API call and get the response.
# 			conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
# 			conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
# 			response = conn.getresponse()
# 			data = response.read()

# 			# 'data' contains the JSON data. The following formats the JSON data for display.
# 			parsed = json.loads(data)
# 			print ("Response:")
# 			print (json.dumps(parsed, sort_keys=True, indent=2))
# 			conn.close()

# 		except Exception as e:
# 			print('Error:')
# 			print(e) 



# cap.release()
# cv2.destroyAllWindows()



