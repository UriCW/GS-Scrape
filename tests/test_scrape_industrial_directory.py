import sys
from ..src import Helpers 
from ..src import DirectoryHarvesters
import json
from time import sleep
from random import randint




def slp():
    """
    Sleep 1 to 10 seconds, this is to not flood their server with requests
    Random to stay less detectable
    """
    sleep(randint(10,30) )


def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def queue_up_industrial_directory():
    base_url="http://www.globalspec.com/industrial-directory/browse/"
    start_page=1
    end_page=500
    letters=[chr(l) for l in range(ord('a'),ord('z')+1) ]
    letters.append("1")

    queue = Helpers.FetchQue("./tmp/ques/industrial_directory.json")
    
    for i,letter in enumerate(letters):
        for page in range(start_page,end_page+1):
            print ("Letter: "+letter+" page "+str(page) )
            html=Helpers.get_directory_page(base_url,letter,page)
            #HTML contains one table, if we're past the last page, the table is empty
            #This is a quick and dirty way to handle this
            if "<tr>" not in html:
                prt("Past last page "+letter+"/"+str(page) )
                break
            jon=DirectoryHarvesters.HarvestIndustrialDirectory().get(html)
            #OK, we've got a list of entries, now queue them
            prt(len(jon))
            for ent in jon:
                ent['harvested']=False
                queue.add(ent)
            #Sleepsome
            slp()
    pass

def test_batch_scrape():
    queue_up_industrial_directory()

def d_test_sleep():
    prt("Starting to sleep")
    slp()
    prt("Wakeup")
