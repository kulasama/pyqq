from algorithm import pwd_encode,get_clientid,get_msgid   
from rest import Get,Post 
import unittest

Headers = {
    'Referer':'http://www.baidu.com/',
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13',
    'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
    'Accept-Language':'zh-cn,zh;q=0.5'
}

class QQ(object) :  
    
    class state:
        status = 'offline'
        vfwebqq = None
        cookie = None
        
    
    def __init__(self,uid,passwd):
        self.uid = uid
        self.passwd = passwd
       
    
   
    def send(self,message):
        pass
        
    def poll(self):
        pass                                         
  
	def _check(self): 
	    url = 'http://ptlogin2.qq.com/check'        
	    params = {
            'uin':self.uid,
        	'appid':1003903,
		} 

        resp,content = Get(url,params = params,headers=Headers)  
        logging.info('check:%s',content)
        self.cookies = Cookie(resp.get('set-cookie',''))
        match = CheckVC.match(content)
        self.verify = match.group('content') 
        return int(match.group('status')),self.verify
        
    def _ptlogin(self):
        url = 'http://ptlogin2.qq.com/login'
        params = {
			'u':self.uid,
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
            
    def login(self): 
        self._check()
        self._ptlogin()     

       
class QQTestCase(unittest.TestCase):

    def test_get_check(self):
    	qq = QQ(1599298566,'helloworld')
    	qq.login()
       


if __name__ == '__main__':
    unittest.main()  
   