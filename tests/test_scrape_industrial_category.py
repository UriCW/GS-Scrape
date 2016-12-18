import sys
from ..src import Helpers 
from ..src import DirectoryHarvesters
import json
from time import sleep
from random import randint


buffer_files="./tmp/queues/industrial_directory.{0}.json"
categories_buffer="./tmp/buffers/categories.json"
catalogs_buffer="./tmp/buffers/catalogs.json"
products_buffer="./tmp/buffers/products.json"


def slp():
    """
    Sleep rand seconds, this is to not flood their server with requests
    Random to stay less detectable
    """
    sleep(randint(0,2) )


def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def d_test_scrape_categories():
    with open( buffer_files.format("index") , 'r') as f:
        jon = json.load(f)
    for j in jon[:20]:#For testing, only few records
        url=j['url']
        category_html=Helpers.get_page(url)
        harv = DirectoryHarvesters.HarvestIndustrialCategory().get(category_html)
        with open(categories_buffer,"a") as f:
            json.dump(harv,f,sort_keys=True,indent=4)
    #We need to do this becuase of json appending arrays above
    #Really, is there no better way? whatever, i'm late enough as it is!
    with open(categories_buffer,"r") as f:
        txt=f.read().replace("][",",")
    with open(categories_buffer,"w") as f:
        f.write(txt)




def test_sort_categories():
    #Tests sorting of a "category page elements" into either product or catalogs for later extraction
    buff_product=[]
    buff_catalog=[]
    with open(categories_buffer,"r") as f: jon=json.load(f)
    for item in jon:
        entry={
            'title' : item['title'],
            'url' : item['url'],
            'comp':item['url'].split("comp=")[1].split("&")[0],
            'vid':item['url'].split("vid=")[1].split("&")[0],
            'partId':item['url'].split("partId=")[1].split("&")[0],
            'harvested':False
        }
        if "partId" in item['url']: # A Products page
            product_entry={
                'title' : item['title'],
                'url' : item['url'],
                'comp':item['url'].split("comp=")[1].split("&")[0],
                'vid':item['url'].split("vid=")[1].split("&")[0],
                'partId':item['url'].split("partId=")[1].split("&")[0],
                'harvested':False
            }
            buff_product.append(product_entry)
        else: #A catalog page
            pass


        if item['cat_id'] is not None:
            prt( "catalog: "+item['cat_id'] )
            item['url']=Helpers.skip_processGlobalSearch(item['url'])
            with open(catalogs_buffer,"a") as f:  
                json.dump(item,f,sort_keys=True,indent=4)
                f.write(",")
        else:
            prt( "product: "+item['title'] )
            buff_product.append(item)
            with open(products_buffer,"a") as f:  
                json.dump(item,f,sort_keys=True,indent=4)
                f.write(",")
    #Again, now we've added a new ',' in the rend, remove it
    with open(products_buffer,"r") as f:
        txt=f.read()
        txt=txt[:len(txt)-1]
        txt="[\n"+txt+"\n]"
    with open(products_buffer,"w") as f:
        f.write(txt)
    with open(catalogs_buffer,"r") as f:
        txt=f.read()
        txt=txt[:len(txt)-1]
        txt="[\n"+txt+"\n]"
    with open(catalogs_buffer,"w") as f:
        f.write(txt)



