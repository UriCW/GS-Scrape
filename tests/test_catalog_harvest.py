import sys
import json
#from ..src.DirectoryHarvesters import *
from ..src.Helpers import *
from ..src import Helpers
from bs4 import BeautifulSoup as bs

def prt(txt):
    sys.stdout.write(str(txt)+"\n")


class HarvestCatalog:
    """
    The content on the search pages is inserted dynamically with json
    eg. http://www.globalspec.com/search/products?page=ms#sqid=19041002&comp=2940&show=products
    lists the contents of json responce to
    http://www.globalspec.com/Search/GetProductResults?sqid=19048503&comp=2940&show=products&origWebHitId=471172407&method=getNewResults

    """
    catalogQue=None
    productQue=None

    def get(self,html):
        """
        Returns a list of either catalogs or products
        Append to relevant que
        
        ret=[
            {
                'title':'',
                'url'  :''
            },...
        ]
        """
        ret=[]
        self.catalogQue=Helpers.FetchQue("./tmp/ques/catalogs.json")
        self.productQue=Helpers.FetchQue("./tmp/ques/products.json")
        soup = bs(html,"html.parser")
        for a in soup.findAll("a"):
            try:
                href=a['href']
                if "search/products" in href: #A catalog
                    entry={
                        'title': a.getText().strip(),
                        'url'  : href, #Need to change this to actual catalog data
                        'harvested' :   False
                    }
                    prt(entry)
                    self.catalogQue.add(entry)
                    ret.append(entry)
                elif "specsearch/partspecs" in href: #A product
                    entry={
                        'title': a.getText().strip(),
                        'product_page'  : href, #Need to change this to actual catalog data
                        'harvested' :   False
                    }
                    self.productQue.add(entry)
                    ret.append(entry)
            except:
                continue
        return ret




def test_catalog():
    #http://www.globalspec.com/search/products?page=ms#sqid=19041002&comp=2940&show=products
    res=load_json_file("./tmp/catalog.content.1.json")
    html=res["RESULTS"]
    HC=HarvestCatalog().get(html)
    prt(HC)
    #assert 1==2
