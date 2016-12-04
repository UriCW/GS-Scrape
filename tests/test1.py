import sys
from bs4 import BeautifulSoup as bs
from ..src.ContentHarvesters import *
def prt(txt):
    sys.stdout.write(str(txt)+"\n")


def get_html_string(fname):
    return open(fname).read()

def test_announcements():
    html=get_html_string("./tmp/suppliers/supplier.productannouncements.ABBElectrificationProducts.html")
    SP = HarvestSupplierProfile()
    ans = SP.getAnnouncements(html)
    #TODO make sure the order doesn't change, IE, that ans[N]['title'] corresponds to the correct ans[N]['desc,url,img]
    #Not sure, but there's a chance that bs gets the order wrong (prob fine though)
    #assert ans[0]['title']=="blah"
    #assert ans[0]['description']=="blah blah blah"
    #assert ans[0]['img']=="blah.png"
    #assert ans[0]['url']=="www.blah.com"
    #assert ans[1]['title'] ==...


def test_articles():
    html=get_html_string("./tmp/suppliers/supplier.techarticles.ABBElectrificationProducts.html")
    SP = HarvestSupplierProfile()
    articles=SP.getArticles(html)
    assert articles[0]['title'] == "The Evolution of the Electronically Controlled Contactor"
    assert articles[0]['url'] == "/Goto/GotoWebPage?gotoUrl=http%3A%2F%2Fwww%2Eglobalspec%2Ecom%2FABBLowVoltageProductsSystems%2Fref%2FEvol%5FElctrnc%5FContctr%2Ehtm&gotoType=TechArticle&vid=98924&context=The%20Evolution%20of%20the%20Electronically%20Controlled%20Contactor&eb=false&fromSupplier=1"




def test_videos():
    html=get_html_string("./tmp/suppliers/supplier.videos.ABBElectrificationProducts.html")
    SP = HarvestSupplierProfile()
    videos=SP.getVideos(html)
    assert videos[0]['title']=="ABB Miniature Circuit Breaker clearing downstream fault ."
    assert videos[0]['url']=="https://www.youtube.com/embed/850aO98OAyI"


class HarvestIndustrialCategory:
    """
    harvest directory shown for items in industrial directory
    e.g /industrial-directory/audio_amplifier_schematic, /industrial-directory/Acrylic_Wrap
    Note, this comes is several (at least two) formats for different categories (the above are different formats for example)
    
    The urls in this directory come like this:
    /search/processGlobalSearch?comp=4352
    /search/processGlobalSearch?comp=2940
    Search?comp=N looks like it's just a redirect to:
    /search/products?page=ms#comp=2940&show=suppliers&sqid=19024082
    i am guessing that sqid is some sql transaction id and is irrelevant for the purpose of scrapping
    it works without, ie
    /search/products?page=ms#comp=2940&show=products
    
    also:
    sometimes link is directly to product! this breaks everything!

    returns
        CatEgories=[
            {
                'title':''
                'cat_id'   :''
                'url'  :''
                'product' : None
            },
        ]
        where title is the title text and id is the component id (?comp=N)
        put in product url too if you can,
        will have to handle this in the next step!
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
            id=url.split("?comp=")[-1]
            #prt( id+" : "+title+":"+url)
            #prt( str(link.prettify() ) )
            cats.append(
                {
                    'id':id,
                    'title':title,
                    'url':url,
                    'product':None
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
            prt( title+";"+str(url) )
            #url=item["href"]
            #id=url.split("?comp=")[-1]
            #prt( id+" : "+title+":"+url)
            #prt( str(link.prettify() ) )
            cats.append(
                {
                    'id':id,
                    'title':title,
                    'url':url,
                    'title':title
                }
            )
        return cats
        

    def get(self,html):
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

def test_industrial_category():
    html=get_html_string("./tmp/industrial_directory/audio_amplifier_schematic.html")
    categories=HarvestIndustrialCategory()
    cats = categories.get(html)
    assert cats[0]['id']==str(2940)
    assert cats[0]['title']=="Audio Amplifiers and Preamplifiers"
    cats=None
    
    html=get_html_string("./tmp/industrial_directory/Acrylic_Wrap.html")
    categories=HarvestIndustrialCategory()
    cats = categories.get(html)
    assert len(cats) > 0
