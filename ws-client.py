#!/usr/bin/python

#python 3.4

import websocket
import _thread
import time
import ssl
import json
import urllib.request


def on_message(ws, message):
#    print (message)
     responseDict=json.loads(message)
#    print("caught an event")
     if responseDict['type']=="MODIFIED":
       for n in responseDict['object']['status']['tags']: 
         if (n['tag']) != "latest":
           print  (n['tag'])
         



def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(30000):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print ("thread terminating...")
    _thread.start_new_thread(run, ())


if __name__ == "__main__":

	# set auth credentials for openshift
	authHeaderKey="Authorization" 
	authHeaderVal="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImplbmtpbnMtc2EtdG9rZW4tMXgxbzAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiamVua2lucy1zYSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImQ1YTg2MTc1LWU3ZWQtMTFlNS05MTAyLTA4MDAyN2I2MTc4YyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmplbmtpbnMtc2EifQ.SZIMjxUdZF9iN3q24lGrylStcZWbWwh8MxcEjD-oeNvK0LnbcmmIhC-jNUkaJyvhSsy2QcKhRM194vMJDY1sCRXAyO26y8bJ-beoS6xOaOUFST3PptnSPemckOkozQImpTy4tZ0hx8ma82UuUAF9wMf4LFy3kornZ6krA38U2k6z05NvB7Y717uQpGQZd2kh4xfHfWcEff3BF9fWZ5U4BuLEgf2t-62JCqYrvnEFxKBo__IL838eXg_hUZySEOUD_Nq9GDAlimnXzm2AxWDFWQfJXt-lS430DUQ1XHwqVq-cL0BrZhZR7sjtHkjtF-6Boq2tvpHtwba1ooIBhXwouQ"

	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	#	SSLContext.verify_mode  CERT_NONE

	# first, get the current version of the resource
	url="https://localhost:8443/oapi/v1/imagestreams"

	request = urllib.request.Request(url)
	request.add_header(authHeaderKey, authHeaderVal)
	responseJson = urllib.request.urlopen(request,context=ctx).read().decode('utf8')

	responseDict=json.loads(responseJson)
#	print (responseJson)
	resourceVersion=responseDict['metadata']['resourceVersion']


	websocket.enableTrace(True)

	ws = websocket.WebSocketApp("wss://localhost:8443/oapi/v1/imagestreams?watch=true&resourceVersion=" + resourceVersion,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
				header = [authHeaderKey + ": " +authHeaderVal])
	#    ws.on_open = on_open

	ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
