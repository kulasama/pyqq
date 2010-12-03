import unittest
import unittest
from  Cookie import SmartCookie as Cookie

def getcookiestr(cookie):
	items = []
	for item in cookie.values():
		if item.key and item.value:
			row = str(item.key)+'='+str(item.value)
			items.append(row)
	return ';'.join(items)

class CookieTestCase(unittest.TestCase):
	
	def test_cookie(self):
		src = """pt2gguin=o0115645232; EXPIRES=Fri, 02-Jan-2020 00:00:00 GMT; PATH=/; DOMAIN=qq.com;, uin=o0115645232; PATH=/; DOMAIN=qq.com;, skey=@MgMxEmEKS; PATH=/; DOMAIN=qq.com;, clientuin=; EXPIRES=Fri, 02-Jan-1970 00:00:00 GMT; PATH=/; DOMAIN=qq.com;, clientkey=; EXPIRES=Fri, 02-Jan-1970 00:00:00 GMT; PATH=/; DOMAIN=qq.com;, zzpaneluin=; EXPIRES=Fri, 02-Jan-1970 00:00:00 GMT; PATH=/; DOMAIN=qq.com;, zzpanelkey=; EXPIRES=Fri, 02-Jan-1970 00:00:00 GMT; PATH=/; DOMAIN=qq.com;, ptisp=ctc;PATH=/; DOMAIN=qq.com;, ptuserinfo=6b756c41;PATH=/;DOMAIN=ptlogin2.qq.com;, ptcz=d94767e7b0fc97bb75a0379ad7ef5e1adc19f3c70edff79159cb55ae85a2f3a0; EXPIRES=Fri, 02-Jan-2020 00:00:00 GMT; PATH=/; DOMAIN=qq.com;, airkey=; EXPIRES=Fri, 02-Jan-1970 00:00:00 GMT; PATH=/; DOMAIN=qq.com;, ptwebqq=8a95fabed6e58868e4b09d5b1e4d8e7d38a6b1faaf2254f20570757ee4b22686; PATH=/; DOMAIN=qq.com;"""
		cookie = Cookie(src)
		print getcookiestr(cookie)			
if __name__ == '__main__':
	unittest.main()
		