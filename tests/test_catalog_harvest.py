import sys
import json
from ..src.DirectoryHarvesters import *
from ..src.Helpers import *
from ..src import Helpers
from bs4 import BeautifulSoup as bs

def prt(txt):
    sys.stdout.write(str(txt)+"\n")


def test_name_convert():
    HC=HarvestCatalog()
    
def test_catalog():
    #http://www.globalspec.com/search/products?page=ms#sqid=19041002&comp=2940&show=products
    res=load_json_file("./tmp/catalog.content.1.json")
    json=res
    HC=HarvestCatalog().get(json)
    #prt(HC)

#http://www.globalspec.com/search/products?page=mi#sqid=19041002&comp=2940&vid=336341
#http://www.globalspec.com/Search/GetSupplierResults?sqid=19041002&comp=2940&vid=336341&origWebHitId=474960224&method=getNewResults
    #assert 1==2
