import sys
import requests
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *
from ..src.Helpers import *

def prt(txt):
    sys.stdout.write(str(txt)+"\n")


def test_product_get():
    url="http://www.globalspec.com/specsearch/partspecs?partId={5BD6F3DA-F4AB-402F-8DB6-8C3F888850BE}&vid=149783&comp=4287&sqid=19039927"
    page=get(url)
    #prt(page)
    assert "CHR" in page
 
