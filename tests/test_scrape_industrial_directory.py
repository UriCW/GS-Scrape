import sys
from ..src import Helpers 
from ..src import DirectoryHarvesters
import json
from time import sleep
from random import randint


buffer_files="./tmp/queues/industrial_directory.{0}.json"
base_url="http://www.globalspec.com/industrial-directory/browse/"

def slp():
    """
    Sleep rand seconds, this is to not flood their server with requests
    Random to stay less detectable
    """
    sleep(randint(0,2) )


def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def buffer_letter(letter, start_page=1, last_page=999):
    buff=[]
    buff_file=buffer_files.format(letter)
    
    for page in range(start_page,last_page):
        html=Helpers.get_directory_page(base_url,letter,page)
        #HTML contains one table, if we're past the last page, the table is empty
        #This is a quick and (very) dirty way to handle this
        if "<tr>" not in html:
            prt("Past last page "+letter+"/"+str(page) )
            return buff
        jon=DirectoryHarvesters.HarvestIndustrialDirectory().get(html) #Jon the J.S.ON.
        buff.append(jon)
        prt(jon)
        with open(buff_file,"a") as bf:
            json.dump(jon,bf, sort_keys=True, indent=4)
    return buff



def queue_up_industrial_directory():
    letters=[chr(l) for l in range(ord('a'),ord('z')+1) ]
    letters.append("1")
    for i,letter in enumerate(letters):
        buff=buffer_letter(letter,1,3) #Only three pages for testing purposes
        slp()





def d_test_merge_files():
    letters=[chr(l) for l in range(ord('a'),ord('z')+1) ]
    letters.append("1")
    buff=[]
    for let in letters:
        fn=buffer_files.format(let)
        with open(fn,"r") as bf:
            txt=bf.read().replace("][",",")
            data=json.loads(txt)
            buff=buff+data
    with open(buffer_files.format("index"),"w") as bf:
        json.dump(buff,bf,sort_keys=True,indent=4)

def d_test_letter_scrape():
    buffer_letter("z",1,3)

def d_test_letters_scrape():
    for let in ['a','b','c']:
        buffer_letter(let,1,5)

def d_test_batch_scrape(): #Harvest all of the industrial directory
    queue_up_industrial_directory()

def d_test_sleep():
    prt("Starting to sleep")
    slp()
    prt("Wakeup")
