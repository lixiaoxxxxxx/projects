from weibo import APIClient
from re import split
import urllib,httplib
import webbrowser
 
 
#APP_KEY = '4126686462'
#APP_SECRET = '33fd8564bbf57ad3194244bc1b65731b'
#CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
#ACCOUNT = '519316166@qq.com'#your email address
#PASSWORD = '1415533226'     #your pw
#
##for getting the authorize url
#client_0 = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#url = client_0.get_authorize_url()
##print url
#
#APP_KEY = '3592643799' #youre app key 
#APP_SECRET = 'b6a68673222039ad16e6d49e0f0cf5dd' #youre app secret  
#CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
#ACCOUNT = '444584958@qq.com'#your email address
#PASSWORD = 'wsdaswad89'     #your pw
#client_1 = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#url = client_1.get_authorize_url()

#APP_KEY = "3818897121"
#APP_SECRET = "bdd38017ca08d8f90af671eeccb033a6"
#CALLBACK_URL = 'http://api.weibo.com/oauth2/default.html'
#ACCOUNT = '491532229@qq.com'
#PASSWORD = '1333688'
#client_2 = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#url = client_2.get_authorize_url()
APP_KEY = '513690955' #youre app key 
APP_SECRET = '75399d00351a588f9a9690aa1003e897' #youre app secret 
CALLBACK_URL = 'http://api.weibo.com/oauth2/default.html'
ACCOUNT = '15902094173'#your email address
PASSWORD = 'wsdaswad89' #your pw
client_2 = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client_2.get_authorize_url()


#for getting the code contained in the callback url
def get_code_2():
    conn = httplib.HTTPSConnection('api.weibo.com')
    postdata = urllib.urlencode     ({'client_id':APP_KEY,'response_type':'code','redirect_uri':CALLBACK_URL,'action':'submit','userId':ACCOUNT,'passwd':PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
    conn.request('POST','/oauth2/authorize',postdata,{'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
    res = conn.getresponse()
    #print 'headers===========',res.getheaders()
    #print 'msg===========',res.msg
    #print 'status===========',res.status
    #print 'reason===========',res.reason
    #print 'version===========',res.version
    location = res.getheader('location')
	#print location
    code = location.split('=')[1]
    conn.close()
	#print code
    return code
