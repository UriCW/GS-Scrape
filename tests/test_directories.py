import sys
from bs4 import BeautifulSoup as bs
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *

def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def get_html_string(fname):
    return open(fname).read()


def test_directory_of_suppliers():
    html = get_html_string("./tmp/AllSuppliers.A.1.html")
    ds = HarvestDirectoryOfSuppliers().get(html)
    #prt(str(ds))
    assert ds is not []
    assert ds[0]['supplier'] == "A-1 Air Compressor Corp."
    assert ds[0]['link'] == "http://www.globalspec.com/supplier/profile/A1AirCompressor"
                    
    assert ds[3]['supplier'] == "A-1 Awards Inc."
    assert ds[3]['link'] == "http://www.globalspec.com/supplier/profile/A1Awards"

def test_industrial_directory():
    html = get_html_string("./tmp/IndDirectory.a.1.html")
    ind = HarvestIndustrialDirectory().get(html)
    assert ind[0]['category']=="audio amplifier schematic"
    assert ind[0]['link']=="http://www.globalspec.com/industrial-directory/audio_amplifier_schematic"

def test_industrial_category():
    #In the case this is a list of suppliers which contains another list of products
    # eg 'audio amplifier schematic' 
    html = get_html_string("./tmp/industrial_directory/audio_amplifier_schematic.html")
    cats = HarvestIndustrialCategory().get(html)
    assert cats[0]['title']=="Audio Amplifiers and Preamplifiers"
    assert cats[0]['url']=="/search/processGlobalSearch?comp=2940"

    #In the case where this is a list of products
    # eg Acrylic Wrap
    prods = HarvestIndustrialCategory().get(html)
    html = get_html_string("./tmp/industrial_directory/Acrylic_Wrap.html")
    prods = HarvestIndustrialCategory().get(html)
    assert prods[0]['title']=="Industrial Tapes - Polyken All Weather Permanent PE Film Tape -- 838"
    assert prods[0]['url']=="http://www.globalspec.com/specsearch/partspecs?partId={1FF99A78-29F0-4DAF-B9F6-D76C30D3E02D}&vid=128929&comp=4287"

def test_products_listing():
    html=""
