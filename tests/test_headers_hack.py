import sys
import requests
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *
from ..src.Helpers import *

def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def test_product_page():
    url="http://www.globalspec.com/specsearch/partspecs?partId={5BD6F3DA-F4AB-402F-8DB6-8C3F888850BE}&vid=149783&comp=4287&sqid=19039927"
    html=get(url)
    page=HarvestProduct().get(html)
    prt(page['title'])
    assert "CHR® BRAND RULON®TAPE PRODUCTS -- R" in page['breadcrumb']


