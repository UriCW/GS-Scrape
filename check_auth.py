from src import Helpers
import requests
if __name__=="__main__":
    #url="http://www.globalspec.com/search/processGlobalSearch?comp=2940" #doesn't work unauthenticated
    #but redirects here authenticated (in browser only):
    #http://www.globalspec.com/search/products?page=ms#comp=2940&show=suppliers&sqid=19078217
    #Which does work (but only with the jacked http headers hack. 
    #Opening the same link twice gives a sequantial sqid, we need to find a way to get at this number for our session
    #In order to bypass the processGlobalSearch which is locked to us this way
    #http://www.globalspec.com/search/products?page=ms#comp=2940&show=suppliers&sqid=19078247
    #http://www.globalspec.com/search/products?page=ms#comp=2940&show=suppliers&sqid=19078248
    #Ok, on closer inspection, it appears that the only difference between having and not having sqid is the order of the items
    #I really hope I am not wrong about this, but afaict this is the case, sqid only effects the order of items
    #We don't care about this, so we can skip the blocked processGlobalSearch altogether :)
    #all we need is to take the comp= argument and pass it to /search/products?...&comp=...


    url="http://www.globalspec.com/search/products?page=ms#comp=2940&show=suppliers"
    session = requests.session()
    headers=Helpers.load_headers("./tmp/ff_headers.txt")
    resp=session.get(url,headers=headers)
    print(resp.url)

