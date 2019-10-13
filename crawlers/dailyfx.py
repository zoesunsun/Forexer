# Crawler for dailyfx
import requests
from queue import Queue
from bs4 import BeautifulSoup as BS
import time

from ..utils import interface

#add headers and cookies(not necessary yet)
cookies = {
    's_sq': 'adviggroupdailyfxcom%252Cadviggroupdailyfxrollup%3D%2526c.%2526a.%2526activitymap.%2526page%253Dwww.dailyfx.com%25253Amarket%252520news%25253Aarticles%2526link%253D2%2526region%253DBODY%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dwww.dailyfx.com%25253Amarket%252520news%25253Aarticles%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.dailyfx.com%25252Fmarket-news%25252Farticles%25252F2%2526ot%253DA',
    '_ga': 'GA1.2.1068203289.1568244335',
    '_gid': 'GA1.2.494556389.1568987128',
    'AAMC_iggroup_0': 'REGION%7C8',
    '_fbp': 'fb.1.1568640199208.1428405271',
    '_gcl_au': '1.1.1118745223.1568244335',
    'aam_uuid': '03524362110042956714564227988932748133',
    's_cc': 'true',
    'AMCV_434717FE52A6476F0A490D4C%40AdobeOrg': '-1303530583%7CMCIDTS%7C18162%7CMCMID%7C07103825093626892243632354109545815642%7CMCAAMLH-1569737267%7C8%7CMCAAMB-1569737267%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1569139667s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18167%7CvVersion%7C3.3.0',
    '__gads': 'ID=e87701681b671991:T=1568244335:RT=1569125231:S=ALNI_MaDU70uqSui2YCi2-L35x4ra1FKCg',
    'dfx-cookies-level': '3',
    'AMCVS_434717FE52A6476F0A490D4C%40AdobeOrg': '1',
    's_ecid': 'MCMID%7C07103825093626892243632354109545815642',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.dailyfx.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
    'Accept-Language': 'zh-cn',
    'Referer': 'https://www.dailyfx.com/market-news/articles',
    'Connection': 'keep-alive',
}


#Function for fetch data from each article's page
def page(url):
    page = requests.get(url).content
    soup =  BS(page,'lxml')
    title = soup.find('h1',class_='dfx-articleHead__header m-0').text
    
    content = soup.find('div',class_='dfx-articleBody__content')#article body
    pureText_content = content.text#Get text from the article body
    
    return title, pureText_content


def get_content():
    article_dict_list = []# Used to sotre collected data

    #visit article list page,i for page number
    html = requests.get('https://www.dailyfx.com/market-news/articles/1').content
    # html = await aiohttp.request('GET', 'https://www.dailyfx.com/market-news/articles/1')
    #turn into soup
    soup = BS(html,'lxml')
    
    #find article list
    articlelist = soup.findAll('a',class_='dfx-articleListItem jsdfx-articleListItem d-flex mb-3')
    
    #loop within articles and find their url(link), postTime, headline(title), content(body)
    for article in articlelist:

        #find the link
        url = article.get('href')
        #get postTime
        postTime = article.find('span', class_='jsdfx-articleListItem__date text-nowrap').get('data-time')
        #covert it into timestamp
        postTime = int(time.mktime(time.strptime(postTime[:19], "%Y-%m-%dT%H:%M:%S")))
        
        #summary = article.find('div',class_='dfx-font-size-3 py-1').text.strip() cannot locate yet
        
        #title, article_body are get through page funtion
        title, pureText_content = page(url)
        
        # queue.put(interface.News(title=title, message=pureText_content, url=url, timestamp=postTime))
        article_dict_list.append(interface.News(title=title, message=pureText_content, url=url, timestamp=postTime))
    return article_dict_list


if __name__ == "__main__":
    print(get_content())
