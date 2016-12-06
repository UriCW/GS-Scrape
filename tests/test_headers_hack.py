import sys
import requests

def prt(txt):
    sys.stdout.write(str(txt)+"\n")

def save_resp(resp, base_name="./tmp/resp"):
    with open(base_name+'.content.html', 'w') as f:
        f.write(str(resp.content) )
    with open(base_name+'.cookies', 'w') as f:
        f.write( str(resp.cookies) )
    with open(base_name+'.headers', 'w') as f:
        f.write( str(resp.headers) )


def load_headers(fname):
    lines=open(fname,"r").readlines()
    ret={}
    for line in lines:
        n=line.split(": ")[0].strip()
        v=line.split(": ")[1].strip()
        ret[n]=v
    return ret


def get(url):
    session = requests.session()
    produrl=url
    headers=load_headers("./tmp/ff_headers.txt")
    resp=session.get(produrl,headers=headers)
    save_resp(resp,"./tmp/get_fake_ff_session")
    return resp.text



def test_product_get():
    url="http://www.globalspec.com/specsearch/partspecs?partId={5BD6F3DA-F4AB-402F-8DB6-8C3F888850BE}&vid=149783&comp=4287&sqid=19039927"
    page=get(url)
    prt(page)
 
