#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 17:38:58 2020

@author: cloveryang
"""

import requests
from bs4 import BeautifulSoup
import csv


class ZillowScraper:
    results = []

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': "zguid=23|%244f681f46-dcaf-446c-9fb3-8352c74e5c90;_ga=GA1.2.2110322994.1599971417;zjs_anonymous_id=%224f681f46-dcaf-446c-9fb3-8352c74e5c90%22;_pxvid=d362e13b-f579-11ea-bccd-0242ac120004;_gcl_au=1.1.1907290269.1599971420;g_state={'i_p':1599978626093,'i_l':1};liveagent_oref=https://www.google.com/;liveagent_ptid=df5dad4e-85d7-4b3d-a83b-a34b3d3d148e; optimizelyEndUserId=oeu1600022315136r0.018125984892192637; FSsampler=371486086; _cs_c=1; liveagent_vc=5; visitor_id701843=158295564; visitor_id701843-hash=0b7b954eceb11ce1348568eea663e6e2033e4e701931577e483e699e7540380a7e7cebba0280cc3e9ecf28658b85ac5b12867a73; DoubleClickSession=true; _cs_id=2616d89a-39b7-a875-ddc9-dd98f08bf505.1600022318.4.1600294482.1600294482.1.1634186318291.Lax.0; __CT_Data=gpv=3&ckp=tld&dm=zillow.com&apv_82_www33=3&cpv_82_www33=3; ctm={'pgv':3626279308820788|'vst':7349592143593083|'vstr':6160709337173637|'intr':1600294961258|'v':1|'lvst':4444}; zgsession=1|b1dc832f-8e6e-4202-a955-1014b40cbe78; _gid=GA1.2.466249192.1600792318; KruxPixel=true; KruxAddition=true; ki_s=; ki_r=aHR0cHM6Ly93d3cuc2NyYXBlaGVyby5jb20vaG93LXRvLXNjcmFwZS1yZWFsLWVzdGF0ZS1saXN0aW5ncy1vbi16aWxsb3ctY29tLXVzaW5nLXB5dGhvbi1hbmQtbHhtbC8%3D; ki_t=1600792336293%3B1600792336293%3B1600808530370%3B1%3B26; G_ENABLED_IDPS=google; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEho66es1y%2FqUdZRuThNsPHkzwLheUZTuqsfLiH8NZ1y8ki6GSsRgAICMhX5rtu6UOqbrR6VUpgki; userid=X|3|5af19e2c810123d4%7C7%7CdTifeUqC39UPjhDzvY7DOSiikSsOJmIMTNB9-8hKBQE%3D;loginmemento=1|84d3f93600ebc08a65b8c49a57e748c912b4e8cd6a89eac7f0d61e5883465e87;ZILLOW_SSID=1|AAAAAVVbFRIBVVsVEgdmxmBIFZYRk039aXrYQrrmc8FMBCwAka7nczeTJ2k7evXULDO%2BqamtZQSnpv%2B0xHG7bs8ZuRg4;zjs_user_id=%22X1-ZU14nmswbv5mxop_9abc3%22;JSESSIONID=7F84306FA2E3FC8D7A1CE61CFB8CC828;_uetsid=09fe6f943cc0ae1686e87307b79a862c;_uetvid=62b31459af1a3d7fe9086ff56637a132;_derived_epik=dj0yJnU9SmhmbllVeDkwTGZmM2hZTG95RllmVWhXT3JlbUdOSEcmbj0tY1RxTkpVSXR1YWV0VUo2V0kzUmVnJm09NyZ0PUFBQUFBRjlxY2lZ;_pin_unauth=dWlkPU5UQmxNRGhqTXpRdE5XSXhaQzAwWkdJeExUZ3pORFl0Wm1abE5tVXlaRGxrWm1JMSZycD1kSEoxWlE;intercom-session-xby8p85u=TDcxS1hReHZCK1k3dHdUcFE0VnJXbXNLaTVKTXE5K2pscWF4VFlDWmh0ekZLNVR3ZFNXSUZ2T2oyNkRvTUxIOS0tdHNSM2EzYjgreFExMStGT1E0UzVDZz09--c5e05cb9a09948cabdf71c0aa22fdcab344a47b8;AWSALB=SAkffNoyyfDrQWvIZ4FbLejvQl3wB3JSPRNTK6xkvZFgRFsMVy07Kc1C+CjKvQTP4cJCuIhUwWaxCdZmhzIiZnDF9tN36l/VJg0cFNWpFhweo84uPf45AxzuV0hz;AWSALBCORS=SAkffNoyyfDrQWvIZ4FbLejvQl3wB3JSPRNTK6xkvZFgRFsMVy07Kc1C+CjKvQTP4cJCuIhUwWaxCdZmhzIiZnDF9tN36l/VJg0cFNWpFhweo84uPf45AxzuV0hz;search=6|1603403599573%7Crect%3D40.63468195850491%252C-79.67964455078128%252C40.25792721551524%252C-80.24544044921878%26rid%3D26529%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D0%26lt%3Dfsbo%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0926529%09%09%09%09%09%09;_px3=a38087fa17c9185f3ad58ee566f9cf8fbcc845ba5ddf6c27d4866b677c8bbccc:Lnc69O5XIBnKiLT/kl20zGQgbp9GQNXqYhsdpyb/aU8v4MgQomb1N6RDE4B3YBIv1IQGm3u1eKqYfKuTNBO+Qg==:1000:pxWaGhugdi9ViUvAnYhnBQ7+S6oNkwSzGVCIKSWgflDi1CUmDN5dqXATa92WvlQ4oW9zZCyt4rmgaZ4GGhBmhxofy75Z9OgtyU/jksIDzQ1ZxsTZtSC4IY9mxEUHSKBSnvB6YV8OceYqdcqtd0Y4H+2of2qPvPLPxAnA9rp5yaE=",
        'referer': 'https://www.zillow.com/homedetails/345-Waldorf-St-Pittsburgh-PA-15214/11270282_zpid/',
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
            try:
                ba = card.find('ul', {'class': 'list-card-details'}).findAll('li')[1].text.split(' ')[0]
            except:
                ba = 'N/A'
            
            try:
                sqft = card.find('ul', {'class': 'list-card-details'}).findAll('li')[2].text.split(' ')[0]
            except:
                sqft = 'N/A'
            
            try:
                image = card.find('img')['src']
            except:
                image = 'N/A'

            self.results.append({
                'price': card.find('div', {'class': 'list-card-price'}).text,
                'address': card.find('address', {'class': 'list-card-addr'}).text,
                'bds': card.find('ul', {'class': 'list-card-details'}).findAll('li')[0].text.split(' ')[0],
                'ba': ba,
                'sqft': sqft,
                'image': image
            })
    
    def to_csv(self):
        with open('zillow_for_sale.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
        
    def run(self):
        for page in range(1, 5):
            params = {
                'searchQueryState': '{"pagination":{},"usersSearchTerm":"Pittsburgh, PA","mapBounds":{"west":-80.24509712646487,"east":-79.67998787353518,"south":40.25792721551524,"north":40.63468195850491},"mapZoom":11,"regionSelection":[{"regionId":26529,"regionType":6}],"isMapVisible":false,"filterState":{"pmf":{"value":false},"fore":{"value":false},"sort":{"value":"globalrelevanceex"},"auc":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"pf":{"value":false},"fsba":{"value":false}},"isListVisible":true}'
            }
            
            
            
            res = self.fetch('https://www.zillow.com/homes/Pittsburgh,-PA_rb/', params)
            self.parse(res.text)

        self.to_csv()
        

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()
