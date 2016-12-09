import sys
import urllib.request
import requests
import warnings
import json




class FetchQue:
    """
    Handle queing extracted addresses for later extraction
    Initilize given a que file 
    """
    qued=[]
    que_file=None

    def __init__(self,que_file):
        self.qued=load_json_file(que_file)
        self.que_file=que_file

    def add(self,item):
        if not any(d['url'] == item['url'] for d in self.qued):
            self.qued.append(item)
            save_json_file(self.qued,self.que_file)

    def save(self):
        save_json_file(self.qued,self.que_file)
        
            
    

def save_json_file( obj, file_name):
    """
    Save to json file
    """
    with open(file_name,"w") as f:
        json.dump(obj,f, sort_keys=True, indent=4)

def load_json_file(fname):
    """
    Loads a json file
    """
    with open(fname,"r") as json_data:
        ret = json.load(json_data)
    return ret

def get(url):
    """
    Gets an html at url using the browser headers
    """
    session = requests.session()
    headers=load_headers("./tmp/ff_headers.txt")
    resp=session.get(url,headers=headers)
    save_resp(resp,"./tmp/debug/get_fake_ff_session")
    return resp.text

def get_redirect(url):
    """
    Gets the redirect address using browser headers
    """
    session = requests.session()
    headers=load_headers("./tmp/ff_headers.txt")
    resp=session.head(url,headers=headers,allow_redirects=True)
    save_resp(resp,"./tmp/debug/get_head_fake_ff_session")
    return resp.url


def get_json(url):
    """
    Gets a json from a url
    jsons of the product catalogs are not user protected, no need for headers methinks
    """
    session = requests.session()
    resp=session.get(url)
    save_resp(resp,"./tmp/debug/get.json.session")
    return resp.json()


def get_from_file(fname):
    """
    Reads an html file and returns it
    """
    return open(fname).read()


def get_page(url,cookies=None):
    """
    Returns an html page at url
    Depracated use get(url)
    """
    if cookies is None:
        local_filename, headers = urllib.request.urlretrieve(url)
        html_file = open(local_filename)
        return html_file.read()
    response=urllib.request.get(url,cookies=cookies)
    return response

def save_resp(resp, base_name="./tmp/resp"):
    """
    Saves the response data for manual inspection
    """
    with open(base_name+'.content.html', 'w') as f:
        f.write(str(resp.content) )
    with open(base_name+'.cookies', 'w') as f:
        f.write( str(resp.cookies) )
    with open(base_name+'.headers', 'w') as f:
        f.write( str(resp.headers) )

def load_headers(fname):
    """
    Loads headers from a file
    """
    lines=open(fname,"r").readlines()
    ret={}
    for line in lines:
        n=line.split(": ")[0].strip()
        v=line.split(": ")[1].strip()
        ret[n]=v
    return ret

def get_directory_page(base_url,letter,page):
    """
    Gets a directory page, 
    eg http://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/A/1
    """
    url= base_url+str(letter)+"/"+str(page)
    #print(url)
    return get(url)
    #return get_page(url)

def get_directory_pages(base_url,letters=None,max_pages=101):
    """
    Returns a list of htmls fetched from directory 
    eg 
    arguments
        letters -- a list of letters (default: [A..Z,1] )
        max_pages -- last page to get
    """
    ret=[]
    if letters is None:
        letters=[chr(l) for l in range(ord('A'),ord('Z')+1) ]
        letters.append("1");
    for letter in letters:
        for page in range(1,max_pages+1):
          html=get_directory_page(base_url,letter,page)
          if html is None: 
            warnings.warn("Directory letter "+letter+" page "+page+" does not exist, assuming last page in letter")
            continue
          ret.append(html)
    return ret

def get_url_argument(url,argument):
    """
    Takes a url argument 
    """
    ret=url.split(argument+"=")[1].split("&")[0]
    return ret

def skip_processGlobalSearch(url):
    #WARNNING:
    #This is under the dubious assumption that argument ?sqid effects nothing but the order of items!
    #Don't panic, it does look like it's the case!
    comp=get_url_argument(url,"comp")
    ret="/search/products?page=ms#comp={0}&show=products&sqid=0".format(comp)
    return ret


def convert_link_to_json(url,origWebHitId):
    #Takes a link to an html page and convert it to a request for the json location, adds origWebHitId
    #returns only the URI (no globalspec.com)
    try:
        sqid=url.split("sqid=")[1].split("&")[0].strip() or 0
        comp=url.split("comp=")[1].split("&")[0].strip()
        if "vid=" not in url:
            act_url="/Search/GetProductResults?sqid={0}&comp={1}&show=products&origWebHitId={2}&method=getNewResults".format(sqid,comp,origWebHitId)
        else: #Vendor catalog (of products only? or other catalogs too?)
            vid=url.split("vid=")[1].split("&")[0].strip()
            act_url="/Search/GetSupplierResults?sqid={0}&comp={1}&show=products&origWebHitId={2}&vid={3}&method=getNewResults".format(sqid,comp,origWebHitId,vid)
        return(act_url)
    except Exception as ex:
        print("Missing url arguments for catalog harvester")
        print("url : "+url)
        raise ex
