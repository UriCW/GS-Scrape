import sys
from bs4 import BeautifulSoup as bs
#from ..src import *
#from ..src import HarvestSupplierProfile
#from .src import ContentHarvesters
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


def getVideos(html):
    """
    Gets a list of article headers from an html string
    returns
        Videos=[
            {
                "title":""
                "description":""
                "subtext":""
                "url":""
            },
            {},...
        ]
    """
    Videos=[]
    soup=bs(html,'html.parser')
    content=soup.find("div",attrs={'id':'featured-videos'})
    #TODO (This is just the code for Article getting, needs the correct divs ids classes etc)
    for i,vid in enumerate(content.findAll("div",attrs={'class':'videoPage'})):
        title=vid.find("div",attrs={"class":"feature-title"}).getText().strip()
        desc=vid.find("p")
        subtext=vid.find("div",attrs={"class":"classification"})
        #The above don't have a shared container, take from loop index i
        url = content.findAll("iframe")[i]['src']
        if subtext is not None:
            subtext=subtext.getText().strip()
        if desc is not None:
            desc=desc.getText().strip()
        Videos.append(
            { 
                'title':title,
                'description':desc,
                'subtext':subtext,
                'url':url
            }
        )
    return Videos


def test_videos():
    html=get_html_string("./tmp/suppliers/supplier.videos.ABBElectrificationProducts.html")
    SP = HarvestSupplierProfile()
    videos=getVideos(html)
    assert videos[0]['title']=="ABB Miniature Circuit Breaker clearing downstream fault ."
    assert videos[0]['url']=="https://www.youtube.com/embed/850aO98OAyI"
