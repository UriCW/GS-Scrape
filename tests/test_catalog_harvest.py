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

    def convert_link(self,url,origWebHitId):
        prt("Original url: "+url)

        sqid=url.split("sqid=")[1].split("&")[0].strip()
        comp=url.split("comp=")[1].split("&")[0].strip()
        vid=url.split("vid=")[1].split("&")[0].strip()
        if vid is None: #Not a vendor catalog
            act_url="/Search/GetProductResults?sqid={0}&comp={1}&show=products&origWebHitId={2}&method=getNewResults".format(sqid,comp,origWebHitId,vid)
        else: #Vendor catalog (of products only? or other catalogs too?)
            act_url="/Search/GetSupplierResults?sqid={0}&comp={1}&show=products&origWebHitId={2}&vid={3}&method=getNewResults".format(sqid,comp,origWebHitId,vid)
        prt("Formated url"+act_url)
        return(act_url)


    def get(self,json):
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
        html=json["RESULTS"]
        #needed to convert link to actual json data
        origWebHitId=json["PARAMETERS"]["origWebHitId"] 
        ret=[]
        self.catalogQue=Helpers.FetchQue("./tmp/ques/catalogs.json")
        self.productQue=Helpers.FetchQue("./tmp/ques/products.json")
        soup = bs(html,"html.parser")
        for a in soup.findAll("a",attrs={"class":"product-name"}):
            prt("\n========================\n")
            try:
                href=a['href']
                if "search/products" in href: #A catalog
                    a_url=self.convert_link(href,origWebHitId)
                    prt("Original url: "+href+"\n")
                    entry={
                        'title': a.getText().strip(),
                        'url'  : href,
                        'json_url'  : a_url, #Only some of the catalogs have this
                        'harvested' :   False
                    }
                    prt(entry)
                    self.catalogQue.add(entry)
                    ret.append(entry)
                elif "specsearch/partspecs" in href: #A product
                    entry={
                        'title': a.getText().strip(),
                        'url'  : href, 
                        'harvested' :   False
                    }
                    #prt(entry)
                    self.productQue.add(entry)
                    ret.append(entry)
            except Exception as err:
                raise(Exception("Parsing catalog failed"))
        return ret




def test_catalog():
    #http://www.globalspec.com/search/products?page=ms#sqid=19041002&comp=2940&show=products
    res=load_json_file("./tmp/catalog.content.1.json")
    json=res
    HC=HarvestCatalog().get(json)
    #prt(HC)

def test_name_convert():
    HC=HarvestCatalog()
    

#http://www.globalspec.com/search/products?page=mi#sqid=19041002&comp=2940&vid=336341
#http://www.globalspec.com/Search/GetSupplierResults?sqid=19041002&comp=2940&vid=336341&origWebHitId=474960224&method=getNewResults
    #assert 1==2
