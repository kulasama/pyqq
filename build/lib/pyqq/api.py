#coding:utf8
import unittest
import re
import time
from rest import Get,Post
from algorithm import pwd_encode,get_clientid,get_msgid
from  Cookie import SmartCookie as Cookie
from utils import getcookiestr
import urllib
import json 
import logging


Headers = {
    'Referer':'http://www.baidu.com/',
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13',
    'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
    'Accept-Language':'zh-cn,zh;q=0.5'
}  

CheckVC = re.compile(r"^ptui_checkVC\('(?P<status>\d+)','(?P<content>\S+)'\);$")
CB = re.compile(r"^ptuiCB\('(?P<one>\d+)','(?P<two>\d+)','(?P<url>\S+)','(?P<three>\d+)','(?P<status>\S+)'\);")




class QQ(object):
    
	def __init__(self,id,passwd):
		self.id = id
		self.passwd = passwd
		self.msg_count = 1
		self.clientid = get_clientid()  
		self.logined = False
	
	@property
	def encodepwd(self):
		return pwd_encode(self.passwd,self.verify)
	
	

	def _check(self):
		url = 'http://ptlogin2.qq.com/check'
		params = {
		    'uin':self.id,
			'appid':1003903
		}
		resp, content = Get(url,params = params,headers=Headers)  
		logging.info('check:%s',content)
		self.cookies = Cookie(resp.get('set-cookie',''))
		match = CheckVC.match(content)
		self.verify = match.group('content')
		return int(match.group('status')),self.verify
		
	def _prelogin(self):
		url = 'http://ptlogin2.qq.com/login'
		params = {
			'u':self.id,
			'p':self.encodepwd,
			'verifycode':self.verify,
			'u1':'http://web2.qq.com/loginproxy.html?strong=true',
			'remember_uin':1,
			'aid':1003903,
			'h':1,
			'ptredirect':0,
			'ptlang':2052,
			'from_ui':1,
			'pttype':1,
			'dumy':'',
			'fp':'loginerroralert',
	    }
		self.cookies['verifysession'] = self.verify
		Headers['Cookie']=self.cookies.output()
		resp,content = Get(url,params=params,headers=Headers)
		self.cookies = Cookie(resp.get('set-cookie',''))
		match = CB.match(content)
		if int(match.group('one')) == 0:
			return True
		else:
			return False
			
	def _channel_login(self):
		url = 'http://web2-b.qq.com/channel/login'
		self.cookies['notifyNewApp'] = 1
		self.cookies['pgv_pvid'] = 1935756508
		self.cookies['pgv_flv'] = '10.1 r103'
		self.cookies['pgv_info'] = 'pgvReferrer=&ssid=s471232060'
		Headers['Cookie']=getcookiestr(self.cookies)
		Headers['Content-Type']='application/x-www-form-urlencoded'
		Headers['Proxy-Connection'] = 'keep-alive'
		Headers['Referer'] = 'http://web2-b.qq.com/proxy.html?v=20101025002'
		Headers['Origin'] = 'http://web2-b.qq.com'
		Headers['Accept-Encoding'] = 'gzip,deflate,sdch'
		
		body =r"r=%7B%22status%22%3A%22%22%2C%22ptwebqq%22%3A%22"+self.cookies['ptwebqq'].value+r"%22%2C%22passwd_sig%22%3A%22%22%2C%22clientid%22%3A%22"+self.clientid+r"%22%7D"
		resp,content = Post(url,body=body,headers=Headers)
		#self.cookies = Cookie(resp.get('set-cookie',''))
		login_data = json.loads(content)    
		if login_data['retcode'] == 0:
		    self.psessionid = login_data['result']['psessionid']
		    self.vfwebqq = login_data['result']['vfwebqq']   
		    return True 
		else:          
		    return False 
		    
	def login(self): 
	    self._check()
	    self._prelogin()
	    self._channel_login() 
	    self.logined = True 
	    time.sleep(1)      
	
	def logout(self): 
	    logging.info('not implement')
	
	def status(self):
	    logging.info('not implement')
	    return {}
	    
	    
	def send(self,to,msg):
	    return self._sendmsg(to,msg) 
	    
	def invite(self,to,msg):
	    self._add_need_verify(to,msg)
	
	def poll(self,state_callback=None,message_callback=None):   
	    '''  
	    buddies_status_changed json:
	    {'poll_type': 'buddies_status_change', 'value': {'status': 'online', 'client_type': 1, 'uin': 50662227}}
	    '''
	    content =  self._channel_poll()  
	    if content:          
	        for item in content: 
	            type = item['poll_type']
	            if type == 'buddies_status_change' and state_callback:
	                value = item['value']
	                status = value['status']
	                uid = value['uin']
	                state_callback(uid,status)  
	            elif type == 'group_message' and message_callback:  
	                qid = item['value']['group_code']
	                uid = item['value']['send_uin'] 
	                msgs = []
	                for row in item['value']['content']:    
	                    if isinstance(row,str) or isinstance(row,unicode):
	                        msgs.append(row) 
	                msg = u' '.join(msgs) 
	                message_callback(qid,uid,msg)
	            else:
	                logging.debug('unkonwn type <%s>',type) 
   
	 

	                
 
	 
	    
	    	    
		    
		
	def _sendmsg(self,to,msg):
		url = 'http://web2-b.qq.com/channel/send_msg'
		send = {}
		send['to']=to
		send['face']=0
		content = []
		content.append(msg)
		msg_config = []
		msg_config.append('font')
		msg_config.append({"name":"\xe5\xae\x8b\xe4\xbd\x93",
		                   "size":"10",
						   "style":[0,0,0],
						   "color":"000000"})
		content.append(msg_config)
		
		send['content']=json.dumps(content)
		send['msg_id'] = get_msgid(self.msg_count)
		send['clientid'] = self.clientid
		send['psessionid'] = self.psessionid
		r = urllib.quote(json.dumps(send))
		body = r'r=%s' % r
		Headers['Cookie']=getcookiestr(self.cookies)
		resp,content = Post(url,body=body,headers=Headers)
		content_dict= json.loads(content)
		if resp['status'] == '200' and content_dict['retcode'] == 0:
		    logging.info('send msg to %d successs!',to)
		    return True                               
		else:
		    logging.error('send msg to %d failure!',to)
		    logging.error('resp:%s content:%s',str(resp),str(content))
		    return False
                                 

		
	
	def _add_need_verify(self,toid,message):
	    url = 'http://web2-b.qq.com/api/add_need_verify'   
	    Headers['Cookie']=getcookiestr(self.cookies)  
	    params  = {
	        'tuin':toid,
	        'myallow':1,
	        'groupid':0,
	        'msg':message,
	        'vfwebqq':self.vfwebqq,
	    }     
	    body = 'r='+json.dumps(params)
	    resp, content = Post(url,body =body,headers=Headers) 
	    
	    
	def _channel_poll(self):
	    url = 'http://web2-b.qq.com/channel/poll'  
	    params = {
	        'clientid':self.clientid, 
	        'psessionid':self.psessionid,
	        't':int(time.time())
	    } 
	    Headers['Cookie']=getcookiestr(self.cookies) 
	    resp,content = Get(url,params=params,headers=Headers) 
	    
	    self.cookies = Cookie(resp.get('set-cookie','')) 
	    content_dict= json.loads(content)   
	    if resp['status'] == '200' and content_dict['retcode'] == 0:
	        return content_dict['result']
	    else:
	        logging.error('resp:%s,content:%s',str(resp),content)
	        return None 
	
	def _channel_poll2(self):
	    url = 'http://d.web2.qq.com/channel/poll2'  
	    params ={
	        'clientid':self.clientid,
	        'psessionid':self.psessionid,
	        't':int(time.time()),
	        'vfwebqq':self.vfwebqq
	    }  
	    Headers['Cookie'] = getcookiestr(self.cookies)
	    resp,content = Get(url,params=params,headers=Headers) 
	    self.cookies=Cookie(resp.get('set-cookie','')) 
	    print resp
	    print content
	
	def _get_single_info2(self):
	    pass
  
	    
	      
		
	def _get_user_friends(self):
		url = 'http://web2-b.qq.com/api/get_user_friends'
		params={
		    'h':'hello',
		    'vfwebqq':self.vfwebqq
		}                         
		body = 'r='+json.dumps(params) 
		Headers['Cookie']=getcookiestr(self.cookies) 
		resp,content = Post(url,body=body,headers=Headers) 
		content_dict= json.loads(content)
		if resp['status'] == '200' and content_dict['retcode'] == 0:
		    return content_dict['result']
		else:
		    logging.error('resp:%s,content:%s',str(resp),content) 
		    return None
	
	def _get_online_buddies(self):
	    url = 'http://web2-b.qq.com/channel/get_online_buddies'
	    params = {
	        'clientid':self.clientid,
	        'psessionid':self.psessionid,  
	        't':int(time.time())  
	    }      
	    Headers['Cookie']=getcookiestr(self.cookies)
	    resp,content = Get(url,params=params,headers=Headers) 
	    content_dict= json.loads(content) 
	    if resp['status'] == '200' and content_dict['retcode'] == 0:   
	        return content_dict['result']
	    else:
	        logging.error('resp:%s,content:%s',str(resp),content)
	        return None 
	    
		
	def get_all_friends(self):
	    return self._get_user_friends()   
	    
	def get_online_friends(self):
	    return self._get_online_buddies()
		
		

def state_changed(uid,status):
   	pass 
  
def message_received(qid,uid,msg):
    pass
		
class QQTestCase(unittest.TestCase):
	
		
	def test_get_check(self):  
	    qid = None
	    pwd = None
        qq = QQ(qid,pwd)
        qq.login()
        qq.get_online_friends()
        qq.get_all_friends()
        while True:
            qq.poll(state_changed,message_received) 
  

if __name__ == '__main__':
	unittest.main()
	
		