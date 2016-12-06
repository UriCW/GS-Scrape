import sys
from bs4 import BeautifulSoup as bs
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *
from ..src.Helpers import *
import urllib.request
import urllib.parse
import warnings
import json
import http.cookiejar

def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def get_html_string(fname):
    return open(fname).read()

from http.client import HTTPSConnection
from base64 import b64encode
def test_cookies():
    name="NSC_mcwt_fohjoffsjoh360_qvcmjd_xfc"
    content='ffffffffaf1f1c1845525d5f4f58455e445a4a423660'
    url=str("globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287")
    values={
        name:content,
    }
    c = HTTPSConnection(url)
    #we need to base 64 encode it 
    #and then decode it to acsii as python 3 stores it as a byte string
    userAndPass = b64encode(b"int@gmx.co.uk:password123").decode("ISO-8859-1")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    #then connect
    c.request('GET', '/', headers=headers)
    #get the response back
    res = c.getresponse()
    # at this point you could check the status etc
    # this gets the page text
    data = res.read()
    prt(data)
