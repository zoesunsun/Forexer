#!/usr/bin/env python
# coding: utf-8


import requests 
from bs4 import BeautifulSoup as BS
import pandas as pd
import time

from ..utils import interface

def get_content():
    # Headers for requests
    headers = {
        'sec-fetch-mode': 'cors',
        'cookie': 'ASP.NET_SessionId=qwugfnonctcn0ennxxqmqcdh; UserSessionId=9b3313a7-3ceb-404a-99f7-5852fa231510; PopupAd_roadblocks=true; atg=; _ga=GA1.2.1424961896.1568886840; _gid=GA1.2.173220235.1568886840; _fbp=fb.1.1568886840005.1630144181; __gads=ID=a1c5c0287bebf580:T=1568886839:S=ALNI_MbJZrFmzWlfACzl2iAUgHyv-t4_-g; cid=1424961896.1568886840',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'content-type': 'application/json; charset=utf-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://www.fxstreet.com/news',
        'authority': 'www.fxstreet.com',
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
    }

    #paramaters for api
    params = (
        ('Take', '100'),#Number of news fetched from the website
        ('FeedIds', '62d504f0-ae31-4d3d-bba5-11fb479d51ae'),
        ('TagIds', '5f91ad8f-26cd-4643-9233-46bd18b03a70,a6744c19-fe88-488f-8044-fb1f574ca818,71f084aa-8636-45a8-b08c-ba41a091be85,31cdfba0-5b00-4e5a-a85c-e083df2689a1,91953627-3e2c-433d-97e3-6a50d83c3f9d,2b905e80-74eb-4224-8163-de2557a73750,a6221cea-1f2f-46c6-a623-bc085412ac4c'),
    )

    # main function for fetch the data
    response = requests.get('https://www.fxstreet.com/api/PostListMultiFeedApi/GetItems', headers=headers, params=params)

    #data are stored in a json format


    article_dict_list=[]
    for item in response.json()['Items']:
        title = item['TitlePlainText'] # Extract title
        url = 'https://www.fxstreet.com/news/'+item['Url'] #Add prefix for the url
        publicTime = int(time.mktime(time.strptime(item['PublicationDate'][:19], "%Y-%m-%dT%H:%M:%S"))) #GMT, conver to timestamp
        content = item['ContentPlainText'] # body of the article
        article_dict_list.append(interface.News(title=title,message=content,url=url,timestamp=publicTime))
    
    #Store the data in excel using pandas.DataFrame as a backup
    df = pd.DataFrame(response.json()['Items'])
    fxs = df[['TitlePlainText','Summary','Url','PublicationDate','ContentPlainText']].copy()
    fxs['Url'] = 'https://www.fxstreet.com/news/'+fxs['Url']
    fxs['PublicationDate'] = fxs['PublicationDate'].apply(lambda x : int(time.mktime(time.strptime(x[:19], "%Y-%m-%dT%H:%M:%S")))) #GMT
    fxs.columns=['title','summary','url','postTime','content']
    fxs.to_excel('excelresources/fxs.xlsx')
    
    return article_dict_list

if __name__ == '__main__':
    print(get_content())
