# Web scraping - Module Section 10.3.3

# imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# set executable path and the URL for scraping
executable_path={'executable_path': ChromeDriverManager().install()}
browser=Browser('chrome', **executable_path, headless=False)  # creates the automated browser window


#Visit the mars NASA news site
url='https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page; wait 1 sec before loading, usually helpful if dynamic, image-heavy website.
browser.is_element_present_by_css('div.list_text', wait_time=1)
html=browser.html
news_soup=soup(html, 'html.parser')
# div.list_text looks for div tag with list_text class. 
slide_elem=news_soup.select_one('div.list_text') 
slide_elem.find('div', class_='content_title')


# Want to get just the text. Use get_text method to pull out the text of the element.
news_title=slide_elem.find('div', class_='content_title').get_text()


# Pull the paragraph text from the summary under the title on the webpage.
news_p=slide_elem.find('div', class_='article_teaser_body').get_text()


# Images - Module Section 10.3.4

# Visit URL
url='https://spaceimages-mars.com/'
browser.visit(url)


# Inspect with DevTools to see that can use button tag.
# Find and click the full image button. It is the 2nd of 3 button tags on the page so index 1.
full_image_elem=browser.find_by_tag('button')[1]  # this is: <splinter.driver.webdriver.WebDriverElement at 0x....>
full_image_elem.click()


# Parse the resulting html with soup
html=browser.html
img_soup=soup(html, 'html.parser') # this is the html from the image that pops up when clicking 'full image' button


# Inspect the html for the image to find tag and class for the actual image.
# Find the relative image url. img tag with class fancybox-image. The get('src') pulls the link to the image.
img_url_rel=img_soup.find('img', class_='fancybox-image').get('src')


# The above is only a partial link. Need to add on how to get to the page itself.
# Utilize f string to get formatting but include the url as it updates.
img_url=f'https://spaceimages-mars.com/{img_url_rel}'


# Scraping Tables - Module Section 10.3.5

# Scrape the entire table with Pandas read_html function
df=pd.read_html('https://galaxyfacts-mars.com/')[0] #index[0] pulls only first table it encounters
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)


# convert table back into html
df.to_html()


# End automated browser session.
browser.quit()




