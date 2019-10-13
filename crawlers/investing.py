#!/usr/bin/env python
# coding: utf-8
#Need to install html2text
import requests
from bs4 import BeautifulSoup as BS
import time
import pandas as pd

#Interface to implement
from ..utils import interface


#add headers and cookies for access to some secured websites like investing.com

cookies = {
    'PHPSESSID': 'q80fhrq302s2rospojo6of3tau',
    'geoC': 'AU',
    'adBlockerNewUserDomains': '1569157524',
    'gtmFired': 'OK',
    'StickySession': 'id.86344462101.301www.investing.com',
    '_ga': 'GA1.2.1383483153.1569157526',
    '_gid': 'GA1.2.905601419.1569157526',
    '_hjid': 'be8dff0e-be9b-4e5a-96e4-98bb9fdd57e2',
    '_fbp': 'fb.1.1569157526407.1008772884',
    'G_ENABLED_IDPS': 'google',
    '__qca': 'P0-1920705725-1569157526664',
    'r_p_s_n': '1',
    'editionPostpone': '1569157530931',
    'SKpbjs-unifiedid': '^%^7B^%^22TDID^%^22^%^3A^%^223b7851ce-22d8-4c51-8dfb-a911d0635ab1^%^22^%^2C^%^22TDID_LOOKUP^%^22^%^3A^%^22FALSE^%^22^%^2C^%^22TDID_CREATED_AT^%^22^%^3A^%^222019-09-22T13^%^3A05^%^3A38^%^22^%^7D',
    'SKpbjs-id5id': '^%^7B^%^22ID5ID^%^22^%^3A^%^22ID5-ZHMOQdEztv3YiqRwKVDQDC65rvUMaWXBxbnEqtvyNw^%^22^%^2C^%^22ID5ID_CREATED_AT^%^22^%^3A^%^222019-09-22T13^%^3A05^%^3A39.825Z^%^22^%^2C^%^22CASCADE_NEEDED^%^22^%^3Atrue^%^2C^%^22ID5ID_LOOKUP^%^22^%^3Afalse^%^2C^%^223PIDS^%^22^%^3A^%^5B^%^5D^%^7D',
    '_VT_content_1983309_2': '1',
    '__gads': 'ID=9112c8968c9682e3:T=1569161279:S=ALNI_Mbg0Z-YPFJz59lITZEjoqzoqBJFPA',
    'floatCounter_1': '1',
    'freewheel-detected-bandwidth': '189',
    'billboardCounter_1': '0',
    'nyxDorf': 'Z2NiOTNlYiA^%^2FaG9mbzxhfTdnMWs1MWJ^%^2BYWJhYTA0',
    'GED_PLAYLIST_ACTIVITY': 'W3sidSI6Im50alEiLCJ0c2wiOjE1NjkxNjkwODIsIm52IjowLCJ1cHQiOjE1NjkxNjg5NjQsImx0IjoxNTY5MTY5MDM0fSx7InUiOiJQRS9UIiwidHNsIjoxNTY5MTY4OTk5LCJudiI6MSwidXB0IjoxNTY5MTY4OTk4LCJsdCI6MTU2OTE2ODk5OH0seyJ1IjoiYURmMiIsInRzbCI6MTU2OTE2ODk2MiwibnYiOjEsInVwdCI6MTU2OTE2ODA1MSwibHQiOjE1NjkxNjg5NjF9XQ..',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}



# Function for fetch data from each article's page
def page(url):
    page = requests.get(url, headers=headers, cookies=cookies).content
    soup =  BS(page,'lxml')
    soup1 = soup.find('section', id = 'leftColumn') # find the parts of website that we want
    title = soup1.find('h1').text
    
    contentsoup = soup1.find('div', class_ = 'WYSIWYG articlePage') # article body
    content = contentsoup.findAll('p')
    text_res = []
    for ct in content:
        text_res.append(ct.text)  # get text from the article body
    puretext = '\n'.join(text_res)
    # get postTime
    postTime = soup.find('div', class_='contentSectionDetails')
    postTime = postTime.find('span').text

    
    return title, puretext, postTime


def get_content():

    article_dict_list = []# Used to store collected data
    adapated_dict_list = []
    for i in range(1): # find the first 50 pages of financial news
        # print('current page:'+str(i)) # counting
        html = requests.get('https://www.investing.com/news/forex-news/'+str(i),headers=headers, cookies=cookies).content # visit article list page,i for page number
        soup = BS(html,'lxml') # turn into soup
        
        # find article list
        articlelistsection = soup.find('div', class_='largeTitle')
        articlelist = articlelistsection.findAll('article', class_='js-article-item articleItem')
        
        # loop within articles and find their url(link), postTime, headline(title), content(body)
        for article in articlelist:
            #find the link
            url = article.find('a').get('href')
            url = 'https://www.investing.com'+ url
            
            #title, article_body are get through page funtion
            title, pureText_content,  postTime = page(url)

            #Adapt to real-time
            adapated_dict_list.append(interface.News(title=title,message=pureText_content,url=url,timestamp=postTime))

            #store them in a dictionary as a record of the table
            articledict={'url':url,'postTime':postTime,'title':title, 'pureText_content':pureText_content,}
            
            #store the record into a lists
            article_dict_list.append(articledict)
            
    # convert from list of dicts to DataFrame
    article_DataFrame = pd.DataFrame(article_dict_list)
    # save into excel file for backup
    article_DataFrame.to_excel('investing.xlsx',index=False)

    #return list of messages
    return adapated_dict_list


if __name__ == '__main__':
    print(get_content())