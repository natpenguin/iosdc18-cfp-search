#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from lxml import html 
import csv
import re
import cfp_persistence_manager as cpm

def main():
    cfps = []
    for i in range(1, 55):
        print(f"""===============================================
               page: {i}
===============================================""")
        rawData = fetchPageData(i)
        cfps = cfps + parseHTML(rawData)

    mongoClient = cpm.cfp_mongo().insert(cfps)
    save_csv(cfps) # デバッグ用

def fetchPageData(page_num):
    data = urlopen("https://fortee.jp/iosdc-japan-2018/proposal?page={0}".format(page_num))
    response = data.read() 
    return response

def parseHTML(rawData):
    rootTree = html.fromstring(rawData)
    cfpsTree  = rootTree.xpath('//div[@class="list-proposal"]')
    cfps = []
    for cfpTree in cfpsTree:
        cfp = CFP.create(cfpTree) 
        cfps.append(cfp);
    return cfps

def save_csv(cfps):
    with open('cfps_before.csv', 'w', newline = '', encoding = 'utf-8-sig') as f:
      writer = csv.DictWriter(f,CFP.csvHeader)
      writer.writeheader()
      writer.writerows(map(lambda x: x.generate_document(), cfps))


class CFP:
    def __init(self):
        self.title = ""
        self.user = ""
        self.talk_type = ""
        self.description = ""
        self.icon_url = ""
        self.twitter_id = ""

    csvHeader = [
            'title',
            'user',
            'talk_type',
            'description',
            'icon_url',
            'twitter_id']

    def generate_document(self):
        return {'title':self.title,
                'user':self.user,
                'talk_type':self.talk_type,
                'description':self.description,
                'icon_url':self.icon_url,
                'twitter_id':self.twitter_id} 

    def desc(self):
        print(f"""-------------------------------------------------------------------
【title】
{self.title}

【user】
{self.user}

【talk_type】
{self.talk_type}

【description】
{self.description}
        
【icon_url】
{self.icon_url}

【twitter_id】
{self.twitter_id}
                """)

    @classmethod
    def create(cls, cfpTree):
        cfp = CFP()
        cfp.title = cfpTree.xpath('./h2/a')[0].text
        
        cfp.talk_type = cfpTree.xpath('./small')[0].text

        user_tmp = cfpTree.xpath('.//div[contains(@class,"top20")]/span')[0].text_content()
        cfp.user = re.sub(r'^(\s|\t|　)+', "", user_tmp)

        description_temp = cfpTree.xpath('./div[contains(@class,"top40")]')[0].text_content() 
        cfp.description = re.sub(r'^(\s|\t|　)+', "", description_temp)

        icon_url_tree = cfpTree.xpath('.//span/img[contains(@class,"inline-avatar")]')
        if len(icon_url_tree) > 0:
            cfp.icon_url = 'https://fortee.jp' + cfpTree.xpath('.//span/img[contains(@class,"inline-avatar")]')[0].get('src')
        else:
            cfp.icon_url = ''

        cfp.twitter_id = cfpTree.xpath('.//span[contains(@class,"left20")]/a')[0].text 
        cfp.desc()
        return cfp

if __name__ == '__main__':
    main()

