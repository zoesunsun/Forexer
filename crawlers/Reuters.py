#!/usr/bin/env python
# coding: utf-8

# start url:
#     
# https://www.reuters.com/news/archive/GCA-ForeignExchange?view=page&page=1&pageSize=10
# 
# maximum pageSize is 10, don't try to change

# In[47]:


import requests
from bs4 import BeautifulSoup as BS
import time
import pandas as pd 

from ..utils import interface


article_dict_list=[]#empty data storage list
adapted_dict_list=[]#Real time application

def get_content():
    for pageid in range(1):#loop the article pages
        # print('current page is:'+str(pageid))#Just for progress monitor
        base_html = requests.get('https://www.reuters.com/news/archive/GCA-ForeignExchange?view=page&page={}&pageSize=10'.format(pageid))
        
        soup = BS(base_html.content,'lxml')
        articlelist = soup.find('div',class_='news-headline-list').find_all('article',class_='story')
        
        for article in articlelist: #loop the article
            url = 'https://www.reuters.com'+article.a.get('href')
            
            #get into page 
            page_html = requests.get(url)
            page_soup = BS(page_html.content,'lxml')
            #get postTime and covert into timestamp
            postTime = page_soup.find('meta',property='og:article:published_time').get('content')
            postTime = int(time.mktime(time.strptime(postTime[:19], "%Y-%m-%dT%H:%M:%S")))
            #get title
            title = page_soup.find('h1',class_='ArticleHeader_headline').text

            #get content
            content_body = page_soup.find('div',class_='StandardArticleBody_body')
            paragraphs = content_body.find_all('p')
            content = ''
            for paragraph in paragraphs:
                content += paragraph.text+'\n' 
            #create dict    
            article_dict = {'title':title,'content':content,'postTime':postTime,'url':url}
            #append to list 
            article_dict_list.append(article_dict)

            #Adapat to real-time:
            adapted_dict_list.append(interface.News(title=title,message=content,url=url,timestamp=postTime))

    #transfer to DataFrame for backup
    # article_DataFrame = pd.DataFrame(article_dict_list)
    #Do some data backup
    # article_DataFrame.to_excel('ruters.xlsx')
    return adapted_dict_list

if __name__ == '__main__':
    print(get_content())



