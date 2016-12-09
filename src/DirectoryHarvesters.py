import sys
from bs4 import BeautifulSoup as bs
from . import Helpers
import json
#from . import HarvestSupplierProfile
#import HarvestSupplierProfile

class HarvestCatalog:
    """
    The content on the search pages is inserted dynamically with json
    eg. http://www.globalspec.com/search/products?page=ms#sqid=19041002&comp=2940&show=products
    lists the contents of json responce to
    http://www.globalspec.com/Search/GetProductResults?sqid=19048503&comp=2940&show=products&origWebHitId=471172407&method=getNewResults
    
    if there is a vid= in the url, this is a vendor catalog, it comes from
    a json at /Search/GetSupplierResults
    eg 
    http://www.globalspec.com/Search/GetSupplierResults?sqid=19041002&comp=2940&vid=335701&origWebHitId=475234156&method=getNewResults
    
    Product pages are under "/specsearch/partspecs?..." 
    """
    catalogQue=None
    productQue=None

    def convert_link(self,url,origWebHitId):
        #Takes a link to an html page and convert it to a request for the json location, adds origWebHitId
        #returns only the URI (no globalspec.com)
        try:
            sqid=url.split("sqid=")[1].split("&")[0].strip() or 0
            comp=url.split("comp=")[1].split("&")[0].strip()
            if "vid=" not in url:
                act_url="/Search/GetProductResults?sqid={0}&comp={1}&show=products&origWebHitId={2}&method=getNewResults".format(sqid,comp,origWebHitId)
            else: #Vendor catalog (of products only? or other catalogs too?)
                vid=url.split("vid=")[1].split("&")[0].strip()
                act_url="/Search/GetSupplierResults?sqid={0}&comp={1}&show=products&origWebHitId={2}&vid={3}&method=getNewResults".format(sqid,comp,origWebHitId,vid)
            return(act_url)
        except Exception as ex:
            print("Missing url arguments for catalog harvester")
            print("url : "+url)
            raise ex


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
            try:
                href=a['href']
                if "search/products" in href: #A catalog
                    a_url=self.convert_link(href,origWebHitId)
                    entry={
                        'title': a.getText().strip(),
                        'url'  : a_url, #Only some of the catalogs have this
                        'harvested' :   False
                    }
                    self.catalogQue.add(entry)
                    ret.append(entry)
                elif "specsearch/partspecs" in href: #A product
                    entry={
                        'title': a.getText().strip(),
                        'url'  : href, 
                        'harvested' :   False
                    }
                    self.productQue.add(entry)
                    ret.append(entry)
            except Exception as err:
                raise(Exception("Parsing catalog failed"))
        return ret





class HarvestDirectoryOfSuppliers:
  """
  Harvest the links from a Directory Of Suppliers HTML and generate a:
  SoupLiars=[
  {
    'supplier' : ''
    'link      : ''
  },...
  ]
  """
  SoupLiars=[]

  def get(self,html):
    soup = bs(html,'html.parser')
    suppliers=soup.findAll("tr",attrs={"class":"result-item"})
    if suppliers is None: return None #This is past the last page
    for s in suppliers:
      a=s.find("a")
      link=a['href']
      name=a.getText().strip()
      entry={
        "supplier":str(name),
        "link":str(link)
      }
      self.SoupLiars.append(entry)
    return self.SoupLiars
  
  def getPage(self,letter,page):
    #TODO move to helpers and finish
    #Gets a page html text using the format self.BASE_URL+"/"+letter+"/"+page
    #Returns None if past last page
    return None
  def harvest(self):
    letters=[chr(l) for l in range(ord('A'),ord('Z')+1) ]
    letters.append("1");
    for letter in letters:
      for page in range(1,101):
        html=self.getPage(letter,page)
        if html is None: 
          continue
        self.harvestSuppliersFromPage(html)


class HarvestIndustrialDirectory:
    """
    Harvest an industrial directory page
    eg, /industrial-directory/browse/a/1

    ProdActs=[
        {
            'title'  : '',
            'url'      : ''
        },...
    ]
    """
    ProdActs=[]
    
    def get(self,html):
        ret=[] #Stop using self.ProdActs!
        soup = bs(html,'html.parser')
        div=soup.find("div",attrs={'id':'keyword-results'})
        links=div.findAll('a')
        for link in links:
          category=link.getText().strip()
          url=link['href']
          entry={
            'title':str(category),
            'url':str(url),
          }
          ret.append(entry)
          #self.ProdActs.append(entry)
        #return self.ProdActs
        return ret


    """
    To Deprecate (change and move to helpers)
    """

    def testGetPage(self,letter,page):
        #TODO change this to properly get the urls instead of test files
        fname="./tmp/IndDirectory."+letter+"."+str(page)+".html"
        try:
          txt=open(fname).read()
          return txt
        except:
          return None
    def harvest(self):
        letters=[chr(l) for l in range(ord('a'),ord('z')+1) ]
        letters.append("1");
        for letter in letters:
          for page in range(1,101):
            html=self.testGetPage(letter,page)
            if html is None: 
              continue
            self.get(html)


class HarvestIndustrialCategory:
    """
    harvest directory shown for items in industrial directory
    e.g /industrial-directory/audio_amplifier_schematic, /industrial-directory/Acrylic_Wrap
    Note, this comes is several (at least two) formats for different categories (the above are different formats for example)
    
    The urls in this directory come like this for the first format (getFromFormatA):
    /search/processGlobalSearch?comp=4352
    /search/processGlobalSearch?comp=2940
    Search?comp=N looks like it's just a redirect to:
    /search/products?page=ms#comp=2940&show=suppliers&sqid=19024082
    i am guessing that sqid is some sql transaction id and is irrelevant for the purpose of scrapping
    it works without, ie
    /search/products?page=ms#comp=2940&show=products
    
    also:
    sometimes link is directly to product page
    ie http://www.globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287
    will stick the url in product_page in this case, will have to handle this logic in the next step!

    returns
        CatEgories=[
            {
                'title':''
                'cat_id'   :''
                'url'  :''
                'product_page' : None
            }, ...
        ]
        where title is the title text and cat_id is the component id (?comp=N)
        put in product url too if you can
    """
    CatEgories=[]

    def getFromFormatA(self,content):
        """
        e.g /industrial-directory/audio_amplifier_schematic
        I Hate this!
        @TODO change param from ?show=suppliers to ?show=products
        """
        cats=[]
        for i,link in enumerate( content.findAll("a",attrs={'class':'search-result-title'}) ):
            title=link.getText().strip()
            title=' '.join(title.split())
            url=link["href"]
            cid=url.split("?comp=")[-1]
            #prt( id+" : "+title+":"+url)
            #prt( str(link.prettify() ) )
            cats.append(
                {
                    'cat_id':cid,
                    'title':title,
                    'url':url,
                    'product_page':None
                }
            )
        return cats
    def getFromFormatB(self,content):
        """
        e.g. /industrial-directory/Acrylic_Wrap
        I Hate this more!   
        """
        cats=[]
        for item in content.findAll("li",attrs={'class':'part-summary'}):
            title=item.find("div",attrs={"class":"part-name"}).getText().strip()
            title=' '.join(title.split())
            url=item.find("div",attrs={"class":"part-name"}).find("a")["href"]
            cats.append(
                {
                    'cat_id':None,
                    'title':title,
                    'url':url,
                    'product_page':url
                }
            )
        return cats

    def get(self,html):
        #Takes an HTML page, and tried to extract the Categories page or Product Links,
        #This depends on the HTML page
        #Raises exception when not a known HTML format, d/k what to do next stop everything
        soup=bs(html,'html.parser')
        cats=[]
        content=soup.find("div",attrs={"id":"products"})
        if content is not None:
           cats = self.getFromFormatA(content)
           return cats 
        content=soup.find("div",attrs={"class":"simple-section-wrapper"})
        if content is not None:
            cats=self.getFromFormatB(content)
            return cats 
        raise(Exception("Unknown Categories Directory HTML Format"))
