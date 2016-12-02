from bs4 import BeautifulSoup as bs
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

  def dump(self):
    for ent in self.SoupLiars:
      print(ent)



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

class HarvestSupplierProfile:
  def __init__(self):
    pass
  
  Profile={}

  def getHTML(self,supplier_name,category):
    """
    Gets the HTML page for the supplier and category, currently look in ./tmp/suppliers for data
    @TODO get this from URL
    """
    ret=open("./tmp/suppliers/supplier."+category+"."+supplier_name+".html").read()
    return ret
  def getAbout(self,html):
    soup=bs(html,'html.parser')
    content=soup.find("div",attrs={'id':'main-content'})

    title=content.find("div",attrs={'class':'page-title-container'}).find("h1").getText()
    profile_text=content.find("div",attrs={'id':'sp-profile-text'})
    about_video=content.find("div",attrs={'class':'sup-about-video'}).find('iframe')['src']
    about={
      'title':title,
      'text':profile_text,
      'video':about_video
    }
    return about
  def getCatalog(self,html):
    soup=bs(html,'html.parser')
    content=soup.find("div",attrs={'id':'catalog-area-list'})
    catalog=[]
    for div in content.findAll('div',attrs={'class','catalog-area'}):
      url=div.find('a')['href']
      img=div.find('img')['src']
      title=div.find('div',attrs={'class':'area-text'}).find('a').getText().strip()
      subtext=div.find('div',attrs={'class':'subtext'}).getText().strip()
      product={
        'url':url,
        'img':img,
        'title':title,
        'subtext':subtext
      }
      catalog.append(product);
    return catalog
  def getNews(self,html):
    soup=bs(html,'html.parser')
    content=soup.find("div",attrs={'class':'area-listing'})
    news=[]
    for item in content.findAll('div',attrs={'class','area-listing-item'}):
      date=item.find('div',attrs={'class':'left'}).getText().strip()
      title=item.find("a",attrs={'class':'item-title'}).getText().strip()
      url=item.find("a",attrs={'class':'item-title'})['href']
      desc=item.find("p").getText().strip()
      news_item={
        'title':title,
        'date':date,
        'link':url,
        'desc':desc
      }
      news.append(news_item)
    return news
      
  def getAnnouncements(self,html):
    #TODO
    soup=bs(html,'html.parser')
    announce=[]
    for ann in soup.findAll('div',attrs={'class','area-listing-item'}):
      print(ann)
      print()
      img=ann.find('div',attrs={'class':'pa-img-wrapper'}).find('img')['src']
      url=ann.find('div',attrs={'class':'pa-img-wrapper'}).find('a')['href']
      #title=ann.find('div',attrs={'class':'item-title-container'})
      #title=ann.find('div')
      #print(title)
  
      #title=ann.find('div',attrs={'class':'item-info'}).find('a').getText().strip()
      #desc=ann.find('div',attrs={'class':'short-desc'}).find('p').getText().strip()
      #print(img+";"+url)



  def harvest(self,supplier_name):
    categories=['about','catalog','news','productannouncements','techarticles','videos']
    for category in categories:
      html=self.getHTML(supplier_name,category)
      if category =="about":
        about=self.getAbout(html)
        self.Profile['about']=about
      if category =="catalog":
        catalog=self.getCatalog(html)
        self.Profile['catalog']=catalog
      if category =="news":
        news=self.getNews(html)
        self.Profile['news']=news
      if category =="productannouncements":
        announce=self.getAnnouncements(html)

  def dump(self):
    print(self.Profile)

if __name__=='__main__':
  DoS=HarvestDirectoryOfSuppliers()
  DoS.harvest()

  IndDir=HarvestIndustrialDirectory()
  IndDir.harvest()

  SP = HarvestSupplierProfile()
  SP.harvest("ABBElectrificationProducts")
  #SP.dump()
