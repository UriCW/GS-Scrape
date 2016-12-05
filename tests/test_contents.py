
import sys
from bs4 import BeautifulSoup as bs
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *
def prt(txt):
    sys.stdout.write(str(txt)+"\n")


def get_html_string(fname):
    return open(fname).read()

"""
Testing of supplier profile
"""


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


def test_profile():
    htmls={
        'about':get_html_string("./tmp/suppliers/supplier.about.ABBElectrificationProducts.html"),
        'catalog':get_html_string("./tmp/suppliers/supplier.catalog.ABBElectrificationProducts.html"),
        'news':get_html_string("./tmp/suppliers/supplier.news.ABBElectrificationProducts.html"),
        'announcements':get_html_string("./tmp/suppliers/supplier.productannouncements.ABBElectrificationProducts.html"),
        'articles':get_html_string("./tmp/suppliers/supplier.techarticles.ABBElectrificationProducts.html"),
        'videos':get_html_string("./tmp/suppliers/supplier.videos.ABBElectrificationProducts.html"),
    }
    profile=HarvestSupplierProfile().get(htmls)
    assert "Memphis, TN 38125 USA" in profile['info']['content']


def test_industrial_category():
    #Test on Format A
    html=get_html_string("./tmp/industrial_directory/audio_amplifier_schematic.html")
    categories=HarvestIndustrialCategory()
    cats = categories.get(html)
    assert cats[0]['cat_id']==str(2940)
    assert cats[0]['title']=="Audio Amplifiers and Preamplifiers"
    cats=None
    
    #Test on Format B
    html=get_html_string("./tmp/industrial_directory/Acrylic_Wrap.html")
    categories=HarvestIndustrialCategory()
    cats = categories.get(html)
    assert len(cats) > 0
    assert cats[0]['title']=="Industrial Tapes - Polyken All Weather Permanent PE Film Tape -- 838"
    assert cats[0]['url']=="http://www.globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287"
    assert cats[0]['product_page']=="http://www.globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287"
    
    assert cats[5]['title']=="Acoustic Enclosures - ClearSonic IsoPac (Isolation Packages) -- ISOPAC A"
    assert cats[5]['url']=="http://www.globalspec.com/specsearch/partspecs?partId={1805EFD7-3569-42A5-A8B3-BA9AAD687A6B}&vid=123534&comp=4007"
    assert cats[5]['product_page']=="http://www.globalspec.com/specsearch/partspecs?partId={1805EFD7-3569-42A5-A8B3-BA9AAD687A6B}&vid=123534&comp=4007"








def test_product():
    html=get_html_string("./tmp/products/838 Datasheet.html")
    prod = HarvestProduct().get(html)
    #prt(prod)
    assert "POLYKEN ALL WEATHER PERMANENT PE FILM TAPE -- 838" in prod['breadcrumb']
    assert "Polyken All Weather" in prod['title']
    assert "Sealing. Seal, patch,wrap, and splice" in prod['content']
    assert "/GoTo/GoToWebPage?Context=Part:Polyken+All+Weather+Permanent+PE+Film+Tape+--+838&gotoURL=http%3A%2F%2Fcatalog.berryplastics.com%2Fproducts%2Fadhesiv%2Ffilm-tape%2Fadhesiv726838&gototype=TocPartWebPage&VID=128929&Comp=4287&OemId=0" in prod['external']
    assert ".pdf" in prod['datasheet']
    assert prod['product_image'] == "http://partimages.globalspec.com/28/3178/2978178_large.png"
    assert prod['supplier'] == "Berry Plastics Corporation - Engineered Materials Division"

