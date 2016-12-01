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



""" This is my equivelent to TDD :P """
def test_get_page(letter,page):
  """
  This gets a page from the tmp directory, instead of the site,
  It's here to test, The proper one should use urllib or something similar and be in
  HarvestDirectoryOfSuppliers.getPage(letter,page)
  
  Returns a page listing html like at http://BASE_URL/A/1, or None if past last page
  """
  fname="./tmp/AllSuppliers."+letter+"."+str(page)+".html"
  try:
    txt=open(fname).read()
    return txt
  except:
    return None


if __name__=='__main__':
  DoS=HarvestDirectoryOfSuppliers()
  DoS.harvest()

  IndDir=HarvestIndustrialDirectory()
  IndDir.harvest()
  for prod in IndDir.ProdActs:
    print(prod)
#  for s in DoS.SoupLiars:
#    print(s)
  #txt=open("./tmp/AllSuppliers.1.html").read()
  #DoS.harvestSuppliersFromPage(txt)
