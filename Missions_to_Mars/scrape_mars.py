from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import pandas as pd



def latest_news(): 
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # NASA Mars News

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    driver.get(url)

    headlines=driver.page_source
    soup = bs(headlines)

    #pulling the last header 
    heads=soup.find_all("div", class_="content_title")[1].text
    
    latest_header=heads
        
    #scrapping the text paragraph associated to the first header
    paragraph=soup.find_all('div', class_='article_teaser_body')[0].text

    text_dict={}
    text_dict['headers'] = latest_header
    text_dict['paragraph']=paragraph
    
    driver.close()
    return text_dict



# JPL Mars Space Images - Featured Image

def feat_image():
    #repeting the same process with a new url
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url2='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    driver.get(url2)

    picture=driver.page_source
    soup = bs(picture)

    # the class "headerimage is unique in the html file. Then, we'll get the source as "src".
    feat_image=soup.find("img", class_="headerimage").get('src')
    

    #will construct the url by concatenating the two strings
    url2_dummy=url2.replace("index.html","")
    
    final_img_url=url2_dummy+feat_image
    driver.close()

    return final_img_url # this is the final url for the featured image in the website.


# Mars Hemispheres

def hemispheres():
    driver = webdriver.Chrome(ChromeDriverManager().install())

#browsing the titles. The titles are all <h3>.

    url3='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    driver.get(url3)

    hemisphere_titles=driver.page_source
    soup = bs(hemisphere_titles)


    #extracting the 4 hemisphere titles
    c=[]
    hem_names=soup.find_all("h3")

    for x in range(0,len(hem_names)):
        c.append(hem_names[x].text)


    #composing the links that take to the individual hemisphere page
    main_url='https://astrogeology.usgs.gov'
    comp_url=[]

    for y in range(0,8,2):
        acc_link=soup.find_all("a", class_="itemLink product-item")[y].get('href')
        urls4=main_url+acc_link
        comp_url.append(urls4)

    # comp_url This list contains the links for each hemisphere
    

    # Scrapping the links in each individual hemisphere website where the high resolution picture can be downloaded
    enh_pic_url=[]

    for i in comp_url:
        driver.get(i)
        enh_pics=driver.page_source
        soup=bs(enh_pics)
        full_image=soup.find('div', class_="content").a['href']
        enh_pic_url.append(full_image)
    

    #building the requested dictionary

    final_url_name = []

    for i in range(4):
        
        dict = {}
        dict["title"] = c[i]
        dict["img_url"] = enh_pic_url[i]
        
        final_url_name.append(dict)
            
         
    return(final_url_name)

def scrape():
    scrape_dict={'news':latest_news,
    'featured_image'=feat_image,
    'hemispheres'=final_url_name}








