#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from lxml import html 
import csv
import re
import pymongo

def main():
    cfps = []
    for i in range(1, 55):
        print("===============================================")
        print("page: {0}".format(i))
        print("===============================================")
        rawData = fetchPageData(i)
        cfps = cfps + parseHTML(rawData)

    mongoClient = mongo().insert(cfps)
    save_csv(cfps) #デバッグ用？

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
      writer.writerows(map(lambda x: x.generate_document(),cfps))


class CFP:
    def __init(self):
        self.title = ""
        self.user = ""
        self.talk_type = ""
        self.description = "" 
        self.icon_url   = ""
        self.twitter_id    = ""

    csvHeader = ['title','user','talk_type','description','icon_url','twitter_id']

    def generate_document(self):
        return {'title':self.title,'user':self.user,'talk_type':self.talk_type,'description':self.description,'icon_url':self.icon_url,'twitter_id':self.twitter_id} 

    def desc(self):
        print('-------------------------------------------------------------------')
        print('title')
        print(self.title)
        print('\n')

        print('user')
        print(self.user)
        print('\n')

        print('talk_type')
        print(self.talk_type)
        print('\n')

        print('description')
        print(self.description)
        print('\n')

        print('icon_url')
        print(self.icon_url)
        print('\n')

        print('twitter_id')
        print(self.twitter_id)
        print('\n\n')

    @classmethod
    def create(cls, cfpTree):
        cfp = CFP()
        cfp.title = cfpTree.xpath('./h2/a')[0].text
        cfp.talk_type = cfpTree.xpath('./small')[0].text
        before = cfpTree.xpath('.//div[contains(@class,"top20")]/span')[0].text_content()
        cfp.user = re.sub(r'(\s|\t|)', "", before)
        cfp.description = cfpTree.xpath('./div[contains(@class,"top40")]')[0].text_content() 
        icon_url_tree = cfpTree.xpath('.//span/img[contains(@class,"inline-avatar")]')
        if len(icon_url_tree) > 0:
            cfp.icon_url = 'https://fortee.jp' + cfpTree.xpath('.//span/img[contains(@class,"inline-avatar")]')[0].get('src')
        else:
            cfp.icon_url = ''

        cfp.twitter_id = cfpTree.xpath('.//span[contains(@class,"left20")]/a')[0].text 
        cfp.desc()
        return cfp

# モジュール化したほうがよさそ
class mongo:
    def __init__(self):
        # mongodb へのアクセスを確立
        self.client = pymongo.MongoClient('localhost', 27017)
        self.database = self.client.iosdc2018
        self.collection = self.database.cfps

    def insert(self, cfps):
        self.collection.insert_many(map(lambda x: x.generate_document(), cfps))

if __name__ == '__main__':
    main()

