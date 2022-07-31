from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd



def scrape():

    #return dictionary

    big_dict = {}

   
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_url = "https://redplanetscience.com"
    browser.visit(mars_url)
    time.sleep(1)
    #MARS
    mars_html = browser.html
    mars_soup = bs(mars_html, "html.parser")
    mars_articles = mars_soup.find_all('div',class_='list_text')
    for result in mars_articles:
        news_title = result.find('div',class_='content_title').text
        news_p  = result.find('div',class_='article_teaser_body').text

        break
    
    big_dict['title'] = news_title
    big_dict['p'] = news_p

    #JPL
    jpl_url = "https://spaceimages-mars.com"
    browser.visit(jpl_url)
    time.sleep(1)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, "html.parser")

    featured_image_div = jpl_soup.find_all('div',class_='floating_text_area')
    for result in featured_image_div:
        featured_image_location = result.find('a')['href']
    featured_image_url = jpl_url + '/' + featured_image_location

    big_dict['url'] = featured_image_url

    # mars facts
    facts_url = "https://galaxyfacts-mars.com/"
    facts_tables = pd.read_html(facts_url)
    facts_df = pd.DataFrame(facts_tables[1])
    facts_html_table = facts_df.to_html()

    big_dict['table'] = facts_html_table

    #mars hem
    hem_base_url = "https://marshemispheres.com/"
    browser.visit(hem_base_url)
    time.sleep(1)
    hem_base_html = browser.html
    hem_soup = bs(hem_base_html, "html.parser")
    hem_main = hem_soup.find_all('div',class_='item')
    hem_main = hem_soup.find_all('div',class_='item')

    #page list (url)
    hem_page_list = []
    hem_page_title = []

    #gets the link to the pages
    for result in hem_main:
        hem_location = result.find('a')['href']
        hem_title = result.find('h3').text

        hem_url = hem_base_url + hem_location

        hem_page_list.append(hem_url)
        hem_page_title.append(hem_title)

    hem_image_url = []

    for i in hem_page_list:
        browser.visit(i)
        time.sleep(1)
        temp_soup = bs(browser.html, "html.parser")
        temp_path = temp_soup.find('img', class_="wide-image")["src"]

        temp_url = hem_base_url + temp_path
        hem_image_url.append(temp_url)
    
    hemisphere_image_urls = []

    # get number of rows in list (should be same throughout all lists), then create a dictionay for every item in each list

    for i in range(len(hem_image_url)):
        hemisphere_image_urls.append({
            'title': hem_page_title[i],
            'img_url': hem_image_url[i]
    })

    big_dict['dict'] = hemisphere_image_urls
    
    browser.quit()

    # Return results
    return big_dict