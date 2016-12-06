import sys
from bs4 import BeautifulSoup as bs
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *
from ..src.Helpers import *
import urllib.request
import warnings
import json
import http.cookiejar

def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def get_html_string(fname):
    return open(fname).read()

""" Temporarily disabled 
def test_get_dos_batch():
    #Test fetching directory of suppliers pages
    pages=5
    letters=['A','B','X','Y','Z','1']
    dos=[]
    base_url="http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/"
    for i,html in enumerate( get_directory_pages(base_url,letters,pages) ):
        prt(html)
        dir_page=HarvestDirectoryOfSuppliers().get(html)
        dos.append(dir_page)
        json_file="./tmp/dumps/DoS/DoS-"+str(i)+".json"
        save_file(dir_page,json_file)
    save_file(dos,"./tmp/dumps/directory_of_suppliers.json")
"""

""" Temporarily disabled 
def test_get_id_batch():
    #test fetching industrial directory pages
    pages=1
    letters=['a']
    base_url="http://www.globalspec.com/industrial-directory/browse/"
    ind_dir=[]
    for i,html in enumerate( get_directory_pages(base_url,letters,pages) ):
        prt(html)
        dir_page=HarvestIndustrialDirectory().get(html)
        ind_dir.append(dir_page)
        json_file="./tmp/dumps/IndDir/IndDir-"+str(i)+".json"
        save_file(dir_page,json_file)
    save_file(ind_dir,"./tmp/dumps/industrial_directory.json")
"""

def get_product(url):
    """
    Takes a url, 
    eg. http://www.globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287
    needs to be authenticated / set cookies
    returns a product
    """
    html=get_page(url)
    return HarvestProduct().get(html)

def get_industrial_category(url):
    #Tests taking list of industrial category
    #Returns a list which either contains a product or another list
    html=get_page(url)
    return HarvestIndustrialCategory().get(html)

"""
def test_get_ic():
    #Test getting an industrial category (the place industrial directory points to)
    #This can be either a list of products (/industrial-directory/Acrylic_Wrap)
    #Or a list of another list of products (/industrial-directory/audio_amplifier_schematic)
    url="http://www.globalspec.com/industrial-directory/Acrylic_Wrap"
    prt("category page: "+url)
    for entry in get_industrial_category(url):
        if entry['product_page'] is not None:
            prt("product page: "+entry['product_page'] )
            prt("")
            prt("")
            prod=get_product(entry['product_page'])
            #prt(prod)
"""



#The following part require being authenticated
#TODO figure out how this is done
import urllib.parse
import urllib.request
import urllib.response
def get_product_page(url):
    userName = "int@gmx.co.uk"
    passWord  = "password123"
    # create an authorization handler
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, userName, passWord);

    auth_handler = urllib.request.HTTPBasicAuthHandler(p)
    prt(auth_handler)
    opener = urllib.request.build_opener(auth_handler)

    urllib.request.install_opener(opener)

    try:
        result = opener.open(url)
        messages = result.read()
        prt(messages)
    except IOError as e:
        #prt(e)
        prt("Error")

def test_product():
    get_product_page("http://www.globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287")

#def get_cookies():
#    return {
#        'NSC_mcwt_fohjoffsjoh360_qvcmjd_xfc':'ffffffffaf1f1c1845525d5f4f58455e445a4a423660',
#    }



#def test_get_product():
    #cookies=get_cookies()
    #prt(cookies)
    #product_page=get_page("http://www.globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287",cookies)
    #prt(product_page)
    #cj = http.cookiejar.MozzilaCookieJar("./tmp/cookies.txt")
    #prt(cj)
    #pass
    #prt(jar)
