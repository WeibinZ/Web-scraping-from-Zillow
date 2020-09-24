#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:28:20 2020

@author: cloveryang
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import numpy as np


class ZillowScraper:
    results = []

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': "zguid=23|%244f681f46-dcaf-446c-9fb3-8352c74e5c90; _ga=GA1.2.2110322994.1599971417; zjs_anonymous_id=%224f681f46-dcaf-446c-9fb3-8352c74e5c90%22; _pxvid=d362e13b-f579-11ea-bccd-0242ac120004; _gcl_au=1.1.1907290269.1599971420; g_state={'i_p':1599978626093,'i_l':1}; liveagent_oref=https://www.google.com/; liveagent_ptid=df5dad4e-85d7-4b3d-a83b-a34b3d3d148e; optimizelyEndUserId=oeu1600022315136r0.018125984892192637; FSsampler=371486086; _cs_c=1; liveagent_vc=5; visitor_id701843=158295564; visitor_id701843-hash=0b7b954eceb11ce1348568eea663e6e2033e4e701931577e483e699e7540380a7e7cebba0280cc3e9ecf28658b85ac5b12867a73; DoubleClickSession=true; _cs_id=2616d89a-39b7-a875-ddc9-dd98f08bf505.1600022318.4.1600294482.1600294482.1.1634186318291.Lax.0; __CT_Data=gpv=3&ckp=tld&dm=zillow.com&apv_82_www33=3&cpv_82_www33=3; ctm={'pgv':3626279308820788|'vst':7349592143593083|'vstr':6160709337173637|'intr':1600294961258|'v':1|'lvst':4444}; zgsession=1|b1dc832f-8e6e-4202-a955-1014b40cbe78; _gid=GA1.2.466249192.1600792318; KruxPixel=true; KruxAddition=true; ki_s=; ki_r=aHR0cHM6Ly93d3cuc2NyYXBlaGVyby5jb20vaG93LXRvLXNjcmFwZS1yZWFsLWVzdGF0ZS1saXN0aW5ncy1vbi16aWxsb3ctY29tLXVzaW5nLXB5dGhvbi1hbmQtbHhtbC8%3D; G_ENABLED_IDPS=google; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEho66es1y%2FqUdZRuThNsPHkzwLheUZTuqsfLiH8NZ1y8ki6GSsRgAICMhX5rtu6UOqbrR6VUpgki; userid=X|3|5af19e2c810123d4%7C7%7CdTifeUqC39UPjhDzvY7DOSiikSsOJmIMTNB9-8hKBQE%3D; loginmemento=1|84d3f93600ebc08a65b8c49a57e748c912b4e8cd6a89eac7f0d61e5883465e87; ZILLOW_SSID=1|AAAAAVVbFRIBVVsVEgdmxmBIFZYRk039aXrYQrrmc8FMBCwAka7nczeTJ2k7evXULDO%2BqamtZQSnpv%2B0xHG7bs8ZuRg4; zjs_user_id=%22X1-ZU14nmswbv5mxop_9abc3%22; JSESSIONID=7F84306FA2E3FC8D7A1CE61CFB8CC828; _pin_unauth=dWlkPU5UQmxNRGhqTXpRdE5XSXhaQzAwWkdJeExUZ3pORFl0Wm1abE5tVXlaRGxrWm1JMSZycD1kSEoxWlE; _derived_epik=dj0yJnU9dmVxSG9kS1lFQjZDVjlHd1hiZmZCOU9lbUszcmFxQWUmbj1CVnpOTnZSMDByMlBPZFBrUWI2UTd3Jm09NyZ0PUFBQUFBRjlxZWVF; _gat=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_bsco=1; intercom-session-xby8p85u=Y0FwK2F3bzVXUkc2UldhR2N5K2NkQldXSDdoK2VRL1NLV1p5d2dudU81Z3QySnJKeGVEaGNBT1NMamk3cmF5Ny0tVUZoQlRGcmkxOXJMV3lDMVZDa1YwZz09--f446ef79d9f2895638454b4abcf13381bbcdf9a4; _uetsid=09fe6f943cc0ae1686e87307b79a862c; _uetvid=62b31459af1a3d7fe9086ff56637a132; ki_t=1600792336293%3B1600792336293%3B1600813788334%3B1%3B29; AWSALB=iI8SKEcCJYoGo2nWJHyMDzWkEpk0Wx23vlR3DWKEH4f1AqpWHDzW45PJYZMogtRvJ5YS/RZAqjSMapL/vCMNQ2mLtFA2tTot0k29SKjCbEa+bJgKz0YBWWHyJtji; AWSALBCORS=iI8SKEcCJYoGo2nWJHyMDzWkEpk0Wx23vlR3DWKEH4f1AqpWHDzW45PJYZMogtRvJ5YS/RZAqjSMapL/vCMNQ2mLtFA2tTot0k29SKjCbEa+bJgKz0YBWWHyJtji; search=6|1603405788464%7Crect%3D40.63468195850491%252C-79.61750313232425%252C40.25792721551524%252C-80.30758186767581%26rid%3D26529%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D0%26type%3Dhouse%252Ccondo%252Ctownhouse%252Capartment%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0926529%09%09%09%09%09%09; _px3=79be0e6a2c7836ac3af4e6e88ad4161cfa47c02482f70ba50b1ab1d18e407a9a:uBKatk2pG0RxIqd7PryPcSs0RSRpPelvueKWvy+EQdrOjUV804n6Yi1kQ4CKCOqqvYNsD++3vm1uQRTJ4waLCw==:1000:SFWQsnjBaYj59Lg6i4XIi30QsY8SNtsHWcOkGeAdR9MUAn2UDyo9NmFgvr+nJbw7C1PzJI6cctNr/RDyxgGi1lt8PMN3s2OF30C1DZnluOrPMvcpXJfwcngLAzWD7HnqO7/U0IOHdBbMajRl1DoPzOjUMBkfnJJtMdC596uLPv0=",
        'referer': 'https://www.zillow.com/pittsburgh-pa/fsbo/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Pittsburgh%2C%20PA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.30758186767581%2C%22east%22%3A-79.61750313232425%2C%22south%22%3A40.25792721551524%2C%22north%22%3A40.63468195850491%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A26529%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    }

    def fetch(self, url, params):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url, params=params, headers=self.headers)
        print(' | Status code: %s' % res.status_code)
        
        return res
   
    def save_response(self, res):
        with open('res.html', 'w') as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''
        
        with open('res.html', 'r') as html_file:
            for line in html_file:
                html += line
        
        return html
   
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        cards = content.findAll('article', {'class': 'list-card'})
        
        for card in cards:
            # try to extract image
            try:
                image = card.find('div', {'class': 'list-card-top'}).find('img')['src']
            except:
                image = 'N/A'
                
            # extract items
            items = {
                'url': card.find('a', {'class': 'list-card-link'})['href'],
                'details': [
                            price.text for price in
                            card.find('ul', {'class': 'list-card-details'}).find_all('li')
                          ],
                'address': card.find('address', {'class': 'list-card-addr'}).text,
                'image': image
            }
            
            # try to extract price if not extracted yet
            try:
                items['price'] = card.find('div', {'class': 'list-card-price'}).text
            except:
                pass
            
            # append scraped items to results list
            self.results.append(items)
            print(json.dumps(items, indent=2))
    
    def to_json(self):
        with open('zillow_rent.json', 'w') as f:
            f.write(json.dumps(self.results, indent=2))
        
    def run(self):
        for page in range(1, 5):
            params = {
                'searchQueryState': '{"pagination":{},"usersSearchTerm":"Pittsburgh, PA","mapBounds":{"west":-80.30758186767581,"east":-79.61750313232425,"south":40.25792721551524,"north":40.63468195850491},"mapZoom":11,"regionSelection":[{"regionId":26529,"regionType":6}],"isMapVisible":false,"filterState":{"pmf":{"value":false},"fore":{"value":false},"auc":{"value":false},"nc":{"value":false},"fr":{"value":true},"fsbo":{"value":false},"cmsn":{"value":false},"pf":{"value":false},"fsba":{"value":false},"mf":{"value":false},"land":{"value":false},"manu":{"value":false}},"isListVisible":true}'
            }
            
            res = self.fetch('https://www.zillow.com/pittsburgh-pa/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Pittsburgh%2C%20PA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.30758186767581%2C%22east%22%3A-79.61750313232425%2C%22south%22%3A40.25792721551524%2C%22north%22%3A40.63468195850491%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A26529%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D', params)
            self.parse(res.text)

        self.to_json()

df = pd.read_json (r'zillow_rent.json')
df.to_csv (r'zillow_rent.csv', index = None)

rent_data = pd.read_csv("zillow_rent.csv")

df_m = rent_data['details'][rent_data['price'].isnull().values==True]
df_m = df_m.str.lstrip('[\'')
df_m = df_m.str.rstrip('\']')
df_m = df_m.str.split(' ', expand=True)
df_m[0] = df_m[0].str.strip('+')
df_m[3] = df_m[3].str.strip('\'+')
df_m[1]=df_m[1].str.strip('\',')
df_m[2] = df_m[2].str.strip('\',+')
df_m[4] = df_m[4].str.strip('\',')
df_m[5] = df_m[5].str.strip('\',+')
df_m[6] = df_m[6].str.strip('\'+')



if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()




