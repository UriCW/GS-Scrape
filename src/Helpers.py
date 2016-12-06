import sys
import urllib.request
import requests
import warnings
import json
def save_file( obj, file_name):
    """
    Save to json,
    """
    with open(file_name,"w") as f:
        json.dump(obj,f, sort_keys=True, indent=4)


def get(url):
    """
    Gets an html doucment using the browser headers
    """
    session = requests.session()
    produrl=url
    headers=load_headers("./tmp/ff_headers.txt")
    resp=session.get(produrl,headers=headers)
    save_resp(resp,"./tmp/get_fake_ff_session")
    return resp.text

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
    return get_page(url)

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

