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

"""
def test_helpers():
    html=get_directory_page("http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/","A","1")
    dir_of_suppliers=HarvestDirectoryOfSuppliers().get(html)
    prt(dir_of_suppliers)
"""


#""" Temporarily disabled 
def test_get_dos_batch():
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
#"""
def test_get_id_batch():
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


