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

def getArticles(html):
    pass

def test_articles():
    html=get_html_string("./tmp/suppliers/supplier.techarticles.ABBElectrificationProducts.html")
    articles=getArticles(html)
