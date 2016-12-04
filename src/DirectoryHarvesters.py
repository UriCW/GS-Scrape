from bs4 import BeautifulSoup as bs
#from . import HarvestSupplierProfile
#import HarvestSupplierProfile

class HarvestDirectoryOfSuppliers:
  BASE_URL="http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/"

  SoupLiars=[]
  def __init__(self):
    pass

  def genEntry(self,supplier_name,supplier_page_url):
    """ Generates and Returns a dictionary object from parameters (name,link) """
    ret={
      "supplier":supplier_name,
      "link": supplier_page_url
    }
    return ret

  def harvestSuppliersFromPage(self,html):
    soup = bs(html,'html.parser')
    suppliers=soup.findAll("tr",attrs={"class":"result-item"})
    if suppliers is None: return None #This is past the last page
    for s in suppliers:
      a=s.find("a")
      link=a['href']
      name=a.getText()
      entry=self.genEntry(name.strip(),link.strip())
      self.SoupLiars.append(entry)
      
  def getPage(self,letter,page):
    #TODO
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
    ProdActs=[]
    def __init__(self):
        pass

    def harvestProductsFromPage(self,html):
        soup = bs(html,'html.parser')
        div=soup.find("div",attrs={'id':'keyword-results'})
        links=div.findAll('a')
        for link in links:
          product=link.getText().strip()
          url=link['href']
          entry={
            'product':product,
            'link':url
          }
          self.ProdActs.append(entry)

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
            self.harvestProductsFromPage(html)


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
        where title is the title text and id is the component id (?comp=N)
        put in product url too if you can,
    """
    CatEgories=[]

    def getFromFormatA(self,content):
        """
        e.g /industrial-directory/audio_amplifier_schematic
        I Hate this!
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
