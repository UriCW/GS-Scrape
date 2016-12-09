import sys
from ..src import Helpers 
from ..src import DirectoryHarvesters
import json



def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def check_last_page(url,page_number):
    """
    Returns the json contents of url, or None if not found (or no more pages)
    """
    jon=Helpers.get_json(url+"&pg="+str(page_number) ) #Live, use sparsely in dev
    params=url.split('?')[1]
    Helpers.save_json_file(jon,"./tmp/debug/"+params+"&pg="+str(page_number) )
    if "Sorry!" in str(jon['RESULTS']): return None
    else: return jon


def scrape_catalog_pages(root_url):
    cat=DirectoryHarvesters.HarvestCatalog()
    for i in range(0,99):
        prt("\nChecking URL ->"+root_url+" "+str(i) )
        jon=check_last_page(root_url,i)
        if jon==None:
            prt("Scrapped "+str(i)+"pages")
            break
        l=cat.get(jon)
        #prt(l)
    #result=cat.get(root_url)

def scrape_catalogs_que():
    que=Helpers.FetchQue("./tmp/ques/catalogs.json")
    domain="http://www.globalspec.com"
    for ent in que.qued:
        if ent['harvested']==False:
            url=domain+str(ent['url']).strip()
            prt("Harvesting: "+url)
            scrape_catalog_pages(url)
            ent['harvested']=True
            que.save()
        else:
            prt("Already harvested, doing nothing")
            prt(ent['url'])
            continue

def test_harvest_category():
    url="http://www.globalspec.com/industrial-directory/audio_amplifier_schematic"
    cat=DirectoryHarvesters.HarvestIndustrialCategory()
    q=Helpers.FetchQue("./tmp/ques/categories.json")
    html=Helpers.get(url)
    jason=cat.get(html)
    for ent in jason:
        ent['harvested'] = False
        q.add(ent)
    

def d_test_catalogs_que():
    scrape_catalogs_que()


def d_test_scrape_catalog():
    url="http://www.globalspec.com/search/products?page=ms#comp=2940&show=products&sqid=19075256"
    domain="http://www.globalspec.com"
    url=DirectoryHarvesters.HarvestCatalog().convert_link(url,0) #AFAI can tell, origWebHitId url param does nothing (0)
#    url=domain+url
    url=domain+"/Search/GetSupplierResults?sqid=19075256&comp=2940&show=products&origWebHitId=0&vid=402989&method=getNewResults"
    prt(url)
    scrape_catalog_pages(url)
    assert False == True



def d_test_scrape_industrial_category():
    #Audio Amplifiers Schematic
    url="http://www.globalspec.com/industrial-directory/audio_amplifier_schematic"

def d_test_last_page():
    url="http://www.globalspec.com/Search/GetSupplierResults?sqid=19041002&comp=2940&vid=336341&origWebHitId=475514584&method=getNewResults"
    r=check_last_page(url,1)
    prt(r)
    assert 1==2
