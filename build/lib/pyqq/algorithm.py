import hashlib
import random
import unittest
import time

def md5hash(str): 
	return hashlib.md5(str).digest() 

def hex_md5hash(str):
    return hashlib.md5(str).hexdigest().upper() 

def md5hash_3(str):
    return hex_md5hash(md5hash(md5hash(str)))
	
def pwd_encode(pwd,verifyCode): 
    return hex_md5hash(md5hash_3(pwd) + verifyCode.upper())
	
def get_clientid():
	return str(random.randint(0,99))+str(int(time.time())% 1000000)

def get_msgid(id):
	id += 1
	return random.randint(10000000,99999999)
	
class AlgorithmTestCase(unittest.TestCase):

	def test_get_clientid(self):
		print get_clientid()
	
if __name__ == '__main__':
	unittest.main()