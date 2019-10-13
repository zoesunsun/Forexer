#This module require webdriver for chrome, remember to install
import time
import pandas as pd
from selenium import webdriver
from ..utils import interface



def get_content():
    #Initialize the browser
    driver = webdriver.Chrome()
    driver.get("https://twitter.com/forexlive")
    
    #Scroll through the twitter page slowly, allowing it load the data
    for x in range(0, 40):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(0.5)
    #Locate twitter cards use 'js-stream-item.stream-item.stream-item'
    twitters = driver.find_elements_by_class_name('js-stream-item.stream-item.stream-item')

    #Data containers
    twitter_dict_list = []
    adpated_dict_list = []

    # Grab the news title, news content, and release time under each subpage.
    for twitter in twitters:
        try:
            #Test whether there's a news hyperlink
            iframe = twitter.find_element_by_tag_name('iframe')

            #Switch to the content inside to see the fields
            driver.switch_to.frame(iframe)

            #Fileds
            news_title = driver.find_element_by_tag_name('h2').text
            news_body = driver.find_element_by_tag_name('p').text
            url = driver.find_element_by_tag_name('a').get_property('href')

            #Go back to original content
            driver.switch_to.default_content()

        except Exception as e:
            driver.switch_to.default_content()
            news_title = ''
            news_body = ''
            url = ''
        
        #Locate twitter postTime
        postTime = twitter.find_element_by_class_name('time')
        postTime = postTime.find_element_by_tag_name('a').find_element_by_tag_name('span').get_attribute('data-time')
        #Locate twitter topic
        topic = twitter.find_element_by_css_selector('div.js-tweet-text-container')
        topic = topic.find_element_by_tag_name('p')

        #Store in a list of dicts
        twitter_dict = {'topic': topic.text, 'news_title': news_title, 'news_content': news_body, 'postTime': postTime}
        twitter_dict_list.append(twitter_dict)

        #Adapt to real-time versuib
        adpated_dict_list.append(interface.News(title=news_title,message=news_body,url=url,timestamp=postTime))

    #close the brower
    driver.close()
    # Save the data to excel file for backup
    twitter_DataFrame = pd.DataFrame(twitter_dict_list)
    twitter_DataFrame.to_excel('resources/twitter.xlsx', index=False)

    #return the required data to main program
    return adpated_dict_list

if __name__ == "__main__":
    print(get_content())
