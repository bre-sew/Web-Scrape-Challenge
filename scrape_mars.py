#!/usr/bin/env python
# coding: utf-8

# dependencies 
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    # Mission to Mars Challenge
    # NASA Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.

    # identify the target url
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # retrieve the page with the requests module
    response = requests.get(url, verify = True)
    print(response.text)

    # parse and prettify
    soup = bs(response.text,'html.parser')
    print(soup.prettify())

    # print the first news title and summary and assign them to variables
    news_title = soup.find_all('div', class_="content_title")[0].text
    news_title = news_title.strip()
    print(news_title)

    news_p = soup.find_all('div', class_="rollover_description_inner")[0].text
    news_p = news_p.strip()
    print(news_p)


    # JPL Featured Space Image
    # Use splinter to navigate the site and find the image url for the current 
    # Featured Mars Image and assign the url string to a variable called featured_image_url.

    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url2)

    html = browser.html
    soup = bs(html,'html.parser')

    image_url = soup.find('img', class_='headerimage fade-in')['src']
    print(image_url)
    url2_shortened = url2.split("i")[0]

    featured_image_url = url2_shortened + image_url


    # Mars Facts
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts 
    # about the planet including Diameter, Mass, etc. Use Pandas to convert the data 
    # to a HTML table string.

    # use the read html function to scrape the table data
    url = 'https://space-facts.com/mars/'

    marsFacts = pd.read_html(requests.get(url).text)

    mars_df = marsFacts[0]
    mars_df.columns = ["Description","Value"]

    html_table = mars_df.to_html("MarsFactsTable.html")


    # Mars Hemispheres
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar’s hemispheres. 
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image and the Hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(url)

    html = browser.html
    soup = bs(html,'html.parser')

    # identify the items that contain each hemisphere
    marsList = soup.find('div', class_='collapsible results')
    hemisphereItems = marsList.find_all('div', class_='item')
    marsHemispheres = []

    # loop through each identified hemisphere item and pull the title and full image
    for item in hemisphereItems:
        
        # pull the title info for each hemisphere
        hemisphereInfo = item.find('div', class_='description')
        hemisphereTitle = hemisphereInfo.h3.text
        
        # pull the image for each hemisphere
        hemisphereLink = item.find('a')['href']
        
        browser.visit(base_url+hemisphereLink)
        html = browser.html
        soup = bs(html,'html.parser')
        
        hemisphereSRC = soup.find('img', class_='wide-image')['src']
        hemisphereImage = (f"{base_url}{hemisphereSRC}")
        
        print(hemisphereTitle)
        print(hemisphereImage)
        print("-------------------------------------------------------------")
        
        hemDict = {
            "title": hemisphereTitle,
            "image": hemisphereImage
        }
        
        marsHemispheres.append(hemDict)


    browser.quit()

    marsDict = {
        "News_Title": news_title,
        "News_Content": news_p,
        "Mars_Image": featured_image_url,
        "Mars_Facts": html_table,
        "Mars_Hemispheres": marsHemispheres
    }

    return marsDict