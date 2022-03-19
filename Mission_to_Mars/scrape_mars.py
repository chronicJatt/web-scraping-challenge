#################################################
# Import Dependencies & Setup 
#################################################
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# Set executable path and initialise Chromium - Linux Specific
executable_path = {'executable_path': '/usr/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)

#################################################
# NASA Mars News
#################################################
def mars_news(browser):
    # URL to page of scraped
    news_url = 'https://redplanetscience.com/'

    # Visit page with browser
    browser.visit(news_url)

    # Create BeautifulSoup object & parse with lxml
    soup = BeautifulSoup(browser.html, 'lxml')

    # Retrieve the parent div for latest article
    parent_div = soup.find('div', class_='list_text')

    # Scrape results for Latest News Article & Paragraph Text
    news_title = parent_div.find('div', class_='content_title').get_text()
    news_p = parent_div.find('div', class_='article_teaser_body').get_text()

    return news_title, news_p

#################################################
# JPL Mars Space Images - Featured Image
#################################################
def feature_image(browser):
    # URL to page of scraped
    JPL_url = 'https://spaceimages-mars.com/'

    # Visit page with browser
    browser.visit(JPL_url)

    # Find button to full size .jpg and click it
    full_image = browser.find_by_xpath('/html/body/div[1]/div/a')
    full_image.click()

    # Use soup to find image src & save it to variable
    img_soup = BeautifulSoup(browser.html, 'lxml')
    image_url = img_soup.find('img', class_='fancybox-image').get('src')

    # Base URL & img URL to create complete URL
    featured_image_url = JPL_url + image_url

    return featured_image_url

#################################################
# Mars Facts
#################################################
def mars_facts():
    # Use Pandas to scrape the table of planet facts
    mars_df = pd.read_html('https://galaxyfacts-mars.com/')[1]
    mars_df.columns=['Descriptor', 'Value']

    return mars_df.to_html(classes='table')

#################################################
# Mars Hemispheres
#################################################
def hemisphere(browser):
    # Visit Astrogeology website where hi-res images of Mars' hemispheres are stored
    hemisphere_url = 'https://marshemispheres.com/'

    # Visit page with browser
    browser.visit(hemisphere_url)
    
    # List for storing hemisphere dictionaries
    hemisphere_image_urls = []

    # Find and count all images
    images = browser.find_by_css('a.product-item h3')

    # Loop through images, minus one as last a.product-item h3 is not relevant
    for image in range(len(images) - 1):
        # Empty dictionary on each loop
        hemisphere = {}
        # Click the right image on each loop
        browser.find_by_css('a.product-item h3')[image].click()
        # Extract the necessary elements and add to dictionary
        hemisphere['img_url'] = browser.find_by_text('Sample').first['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        # Append dictionary to list
        hemisphere_image_urls.append(hemisphere)
        # Reset page for loop
        browser.back()

    return hemisphere_image_urls

#################################################
# Scrape Function
#################################################
def scrape():
    # Set executable path and initialise Chromium - Linux Specific
    executable_path = {'executable_path': '/usr/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_p = mars_news(browser)
    featured_image_url = feature_image(browser)
    facts_table = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    scrape_time = dt.datetime.now()

    data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'facts_table': facts_table,
        'hemispheres': hemisphere_image_urls,
        'scrape_time': scrape_time
    }
    browser.quit
    return data

if __name__ == '__main__':
    print(scrape())