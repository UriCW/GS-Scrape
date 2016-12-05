import sys
from bs4 import BeautifulSoup as bs
from ..src.ContentHarvesters import *
from ..src.DirectoryHarvesters import *
import urllib.request
def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def get_html_string(fname):
    return open(fname).read()

def get_page(url):
    """
    Returns an html page at url
    """
    local_filename, headers = urllib.request.urlretrieve(url)
    html_file = open(local_filename)
    return html_file.read()


def get_directory_pages(letters=None,max_pages=101):
    """
    Returns a list of htmls fetched from directory of suppliers
    arguments
        letters -- a list of letters (default: [A..Z,1] )
        max_pages -- last page to get
    """
    if letters is None:
        letters=[chr(l) for l in range(ord('A'),ord('Z')+1) ]
        letters.append("1");
    for letter in letters:
        for page in range(1,max_pages):
          #html=self.getPage(letter,page)
          if html is None: 
            continue
          self.harvestSuppliersFromPage(html)




def test_get_directory_of_suppliers():
    letters=['A','B','1']

    html=get_page("http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/A/1")

    prt("html")
    prt(html)
