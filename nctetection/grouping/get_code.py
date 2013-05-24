from weibo import APIClient
from re import split
import urllib,httplib
import webbrowser
 
#APP_KEY = '1398648266' #youre app key 
#APP_SECRET = '91742c83ecf624ce236e14d7bd431245' #youre app secret  
#CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
#ACCOUNT = '526799142@qq.com'#your email address
#PASSWORD = '070343097'     #your pw
#
#client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#url = client.get_authorize_url()
APP_KEY = "3818897121"
APP_SECRET = "bdd38017ca08d8f90af671eeccb033a6"
CALLBACK_URL = 'http://api.weibo.com/oauth2/default.html'
ACCOUNT = '491532229@qq.com'
PASSWORD = '1333688'
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
 

#for getting the code contained in the callback url
def get_code():
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
