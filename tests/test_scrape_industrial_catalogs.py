import sys
from ..src import Helpers 
from ..src import DirectoryHarvesters
import json
from time import sleep
from random import randint

catalogs_buffer="./tmp/buffers/catalogs.json"
products_buffer="./tmp/buffers/products.json"
catalogs="./tmp/output/catalogs.json"

json_catalog_url="http://www.globalspec.com/Search/GetProductResults?comp={0}&show=products&sqid=0&origWebHitId=0&method=getNewResults"

def slp():
    """
    Sleep rand seconds, this is to not flood their server with requests
    Random to stay less detectable
    """
    sleep(randint(0,2) )


def prt(txt):
    sys.stdout.write(str(txt)+"\n")





def test_scrape_catalogs():
    #Scrape the catalogs we got from the category page
    catalogs=[]
    products=[]
    with open(catalogs_buffer,"r") as f:
        jon=json.load(f) #all the catalogs buffered so far
    for j in jon[:2]: #For testing, only few records
        if not 'harvested' in j or j['harvested']==False:
            if j['cat_id'] is None: raise(Exception(" Record missing category id"))
            url=json_catalog_url.format(j['cat_id'])
            prt(url)
            catalog_json=json.loads(Helpers.get_page(url) )
            #prt(catalog_json)
            catalog_harvester=DirectoryHarvesters.HarvestCatalog()
            page_catalogs=catalog_harvester.get_catalogs(catalog_json)
            page_products=catalog_harvester.get_products(catalog_json)
            catalogs.append(page_catalogs)
            products.append(page_products)
            j['harvested']=True
    jon.extend(catalogs)
    #TODO remove duplicates
    with open(catalogs_buffer,"w") as f:
        json.dump(jon,f)
    with open(products_buffer,"r") as f:
        all_products=json.load(f)
    all_products.extend(products)
    with open(products_buffer,"w") as f:
        json.dump(all_products,f)
    
    


