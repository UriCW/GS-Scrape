import sys
from bs4 import BeautifulSoup as bs
from ..src.Harvester import *
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
    #assert articles[0]['title'] == "The Evolution of the Electronically Controlled Contactor"
    #assert articles[0]['url'] == "/Goto/GotoWebPage?gotoUrl=http%3A%2F%2Fwww%2Eglobalspec%2Ecom%2FABBLowVoltageProductsSystems%2Fref%2FEvol%5FElctrnc%5FContctr%2Ehtm&gotoType=TechArticle&vid=98924&context=The%20Evolution%20of%20the%20Electronically%20Controlled%20Contactor&eb=false&fromSupplier=1"
