# Web scraping - Module Section 10.5.3

# imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #initiate headless driver for deployment
    executable_path={'executable_path':ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph=mars_news(browser)

    # Run all scraping fcns and store in dictionary
    data={
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):  #Visit & Scrape the mars NASA news site
    url='https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page; wait 1 sec before loading, usually helpful if dynamic, image-heavy website.
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html=browser.html
    news_soup=soup(html, 'html.parser')
    # div.list_text looks for div tag with list_text class. 
    try:
        slide_elem=news_soup.select_one('div.list_text') 
        # Use get_text method to pull out the text of the element.
        news_title=slide_elem.find('div', class_='content_title').get_text()
        # Pull the paragraph text from the summary under the title on the webpage.
        news_p=slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:  # Error when coding script refers to an invalid attribute
        return None, None
    return news_title, news_p


def featured_image(browser): # Visit URL and scrape image
    url='https://spaceimages-mars.com/'
    browser.visit(url)
    # Find and click the full image button. 
    full_image_elem=browser.find_by_tag('button')[1] 
    full_image_elem.click()

    # Parse the resulting html with soup
    html=browser.html
    img_soup=soup(html, 'html.parser') # this is the html from the image that pops up when clicking 'full image' button

    # Find the relative image url. img tag with class fancybox-image. The get('src') pulls the link to the image.
    try:
        img_url_rel=img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Utilize f string to get formatting but include the url as it updates.
    img_url=f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


def mars_facts():
    # Scrape the entire table with Pandas read_html function
    try:
        df=pd.read_html('https://galaxyfacts-mars.com/')[0] #index[0] pulls only first table it encounters
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    #Convert df into html format and add bootstrap
    return df.to_html(classes="table table-striped")


if __name__=="__main__":
    print(scrape_all())