#coding:utf8
import httplib2
import urllib


def Get(url,params,headers):
	h = httplib2.Http()
	urlparams = urllib.urlencode(params)
	url = url+'?'+urlparams
	resp, content = h.request(url,method='GET',headers=headers)
	return resp,content

def Post(url,params=None,body=None,headers={}):	
	h = httplib2.Http()
	if params:
		body = urllib.urlencode(params)
	elif body:
		body = body
	resp, content = h.request(url, method="POST", body=body,headers=headers)
	return resp,content





		
		
	