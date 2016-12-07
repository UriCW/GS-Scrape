import sys
import json
from ..src.Helpers import *

def prt(txt):
    sys.stdout.write(str(txt)+"\n")

class QueCatalog:
    catalogs=[]
    que_file=None

    def __init__(self,catalogs_file="./tmp/ques/catalogs.json"):
        self.catalogs=load_json_file(catalogs_file)
        self.que_file=catalogs_file

    def add(self,catalog):
        if not any(d['url'] == catalog['url'] for d in self.catalogs):
            self.catalogs.append(catalog)
            save_json_file(self.catalogs,self.que_file)


def test_que_catalog():
    prt("***TESTING QUE***")
    que=QueCatalog()
    ent={"title":"The The", "url":"www.The.The.The", "harvested":False}
    que.add(ent)
    #assert True == False
