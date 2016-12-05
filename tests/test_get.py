import sys
from bs4 import BeautifulSoup as bs
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *
from ..src.Helpers import *
import urllib.request
import warnings
import json
def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def get_html_string(fname):
    return open(fname).read()

def save_file( obj, file_name):
    """
    Save to json,
    """
    with open(file_name,"w") as f:
        json.dump(obj,f)

def get_page(url):
    """
    Returns an html page at url
    """
    local_filename, headers = urllib.request.urlretrieve(url)
    html_file = open(local_filename)
    return html_file.read()

def get_directory_page(base_url,letter,page):
    """
    Gets a directory page, 
    eg http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/A/1
    """
    url= base_url+str(letter)+"/"+str(page)
    return get_page(url)

def get_directory_pages(base_url,letters=None,max_pages=101):
    """
    Returns a list of htmls fetched from directory 
    eg 
    arguments
        letters -- a list of letters (default: [A..Z,1] )
        max_pages -- last page to get
    """
    ret=[]
    if letters is None:
        letters=[chr(l) for l in range(ord('A'),ord('Z')+1) ]
        letters.append("1");
    for letter in letters:
        for page in range(1,max_pages+1):
          #html=self.getPage(letter,page)
          html=get_directory_page(base_url,letter,page)
          prt(html)
          if html is None: 
            warnings.warn("Directory letter "+letter+" page "+page+" does not exist, assuming last page in letter")
            continue
          ret.append(html)
    return ret



"""
def test_get_directory_of_suppliers():
    html=get_directory_page("http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/","A","1")
    dir_of_suppliers=HarvestDirectoryOfSuppliers().get(html)
    prt(dir_of_suppliers)
"""
def test_get_dos_batch():
    letters=['A']
    #letters=['A','B','X','Y','Z','1']
    dos=[]
    base_url="http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/"
    for i,html in enumerate( get_directory_pages(base_url,letters,3) ):
        prt(html)
        dir_page=HarvestDirectoryOfSuppliers().get(html)
        dos.append(dir_page)
        json_file="./tmp/dumps/DoS/DoS-"+str(i)+".json"
        save_file(dir_page,json_file)
    save_file(dos,"./tmp/dumps/directory_of_suppliers.json")

