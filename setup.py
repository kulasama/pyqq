from setuptools import setup     
setup(
        name = 'pyqq',
        version = '0.0.5',
        description = "nsfocus qq client library", 
        long_description="""
            python qq client library
            
            example:
            from pyqq import QQ
            uid = YOUR QQ NUMBER
            pwd = YOUR QQ PASSWORD
            qq = QQ(uid,pwd)
            qq.login()
            while True:
                qq.poll()
        """,
        license = "gpl3",
        author = "kula",
        author_email = "kulasama@gmail.com",  
        url='http://github.com/kulasama/pyqq', 
        tests_require = ['nose'],  
        platforms = 'any',
        packages = ['pyqq',],           
)
