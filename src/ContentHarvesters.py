from bs4 import BeautifulSoup as bs
class HarvestSupplierProfile:
    """
    Harvest data for a single Supplier profile.
    Stores result of harvest in 
    ProFile = {
      'about': ...
      'catalog': ...
      'news': ...
      'announcements': ...
      'articles': ...
      'videos': ...
    }
    """
    ProFile={}
    
    def getHTML(self,supplier_name,category):
      """
      Gets the HTML page for the supplier and category, currently look in ./tmp/suppliers for data
      @TODO get this from URL
      """
      ret=open("./tmp/suppliers/supplier."+category+"."+supplier_name+".html").read()
      return ret
    def getAbout(self,html):
      soup=bs(html,'html.parser')
      content=soup.find("div",attrs={'id':'main-content'})

      title=content.find("div",attrs={'class':'page-title-container'}).find("h1").getText()
      profile_text=content.find("div",attrs={'id':'sp-profile-text'})
      about_video=content.find("div",attrs={'class':'sup-about-video'}).find('iframe')['src']
      about={
        'title':title,
        'text':profile_text,
        'video':about_video
      }
      return about
    def getCatalog(self,html):
      soup=bs(html,'html.parser')
      content=soup.find("div",attrs={'id':'catalog-area-list'})
      catalog=[]
      for div in content.findAll('div',attrs={'class','catalog-area'}):
        url=div.find('a')['href']
        img=div.find('img')['src']
        title=div.find('div',attrs={'class':'area-text'}).find('a').getText().strip()
        subtext=div.find('div',attrs={'class':'subtext'}).getText().strip()
        product={
          'url':url,
          'img':img,
          'title':title,
          'subtext':subtext
        }
        catalog.append(product);
      return catalog
    def getNews(self,html):
      soup=bs(html,'html.parser')
      content=soup.find("div",attrs={'class':'area-listing'})
      news=[]
      for item in content.findAll('div',attrs={'class','area-listing-item'}):
        date=item.find('div',attrs={'class':'left'}).getText().strip()
        title=item.find("a",attrs={'class':'item-title'}).getText().strip()
        url=item.find("a",attrs={'class':'item-title'})['href']
        desc=item.find("p").getText().strip()
        news_item={
          'title':title,
          'date':date,
          'link':url,
          'desc':desc
        }
        news.append(news_item)
      return news
      
    def getAnnouncements(self,html):
      soup = bs(html,"html.parser")
      #There is an extra </div> which breaks everything.
      #Iterate 4 times instead and then join arrays (and hope they are in the same order)
      titles=[]
      descriptions=[]
      images=[]
      urls=[]
      for title in soup.findAll("div",attrs={"class","item-title-container"}):
          titles.append(title.getText().strip() )
          link=title.find("a")['href']
          urls.append(link)
      for desc in soup.findAll("span",attrs={"class","short-desc"}):
          descriptions.append(desc.getText().strip() )
      for img in soup.findAll("div",attrs={"class":"pa-img-wrapper"}):
          src=img.find("img")['src']
          images.append(src)
      #Now put in dictionary
      announcements=[]
      for i in range(0,len(titles)):
          item={}
          item['title']=titles[i]
          item['description']=descriptions[i]
          item['img']=images[i]
          item['url']=urls[i]
          announcements.append(item)
      return(announcements)

    def getArticles(self,html):
      """
      Gets a list of article headers from an html string
      returns
          Articles=[
              {
                  "title":""
                  "description":""
                  "subtext":""
                  "url":""
              },
              {},...
          ]
      """
      Articles=[]
      soup=bs(html,'html.parser')
      content=soup.find("div",attrs={'class':'area-listing'})
      items=content.findAll("div",attrs={'class':'area-listing-item'})
      for item in items:
          title=item.find('a',attrs={'class':'item-title'}).getText().strip()
          url=item.find('a',attrs={'class':'item-title'})['href']
          subtext=item.find("b").getText().strip() 
          desc=item.find("div",attrs={'class':'last'}).find("div").getText().strip()#TODO cleanup
          Articles.append(
              {
                  'title':title,
                  'url':url,
                  'subtext':subtext,
                  'description':desc
              }
          )
      return Articles

    def getVideos(self,html):
        """
        Gets a list of article headers from an html string
        returns
            Videos=[
                {
                    "title":""
                    "description":""
                    "subtext":""
                    "url":""
                },
                {},...
            ]
        """
        Videos=[]
        soup=bs(html,'html.parser')
        content=soup.find("div",attrs={'id':'featured-videos'})
        #TODO (This is just the code for Article getting, needs the correct divs ids classes etc)
        for i,vid in enumerate(content.findAll("div",attrs={'class':'videoPage'})):
            title=vid.find("div",attrs={"class":"feature-title"}).getText().strip()
            desc=vid.find("p")
            subtext=vid.find("div",attrs={"class":"classification"})
            #The above don't have a shared container, take from loop index i
            url = content.findAll("iframe")[i]['src']
            if subtext is not None:
                subtext=subtext.getText().strip()
            if desc is not None:
                desc=desc.getText().strip()
            Videos.append(
                { 
                    'title':title,
                    'description':desc,
                    'subtext':subtext,
                    'url':url
                }
            )
        return Videos


    def harvest(self,supplier_name):
        categories=['about','catalog','news','productannouncements','techarticles','videos']
        for category in categories:
          html=self.getHTML(supplier_name,category)
          if category =="about":
            about=self.getAbout(html)
            self.ProFile['about']=about
          if category =="catalog":
            catalog=self.getCatalog(html)
            self.ProFile['catalog']=catalog
          if category =="news":
            news=self.getNews(html)
            self.ProFile['news']=news
          if category =="productannouncements":
            announce=self.getAnnouncements(html)
            self.ProFile['announcements']=announce
          #TODO add remaining categoried here!

class HarvestProduct:
    pass
