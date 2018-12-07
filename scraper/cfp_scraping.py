#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from lxml import html 
import csv
import re
import cfp_persistence_manager as cpm
import datetime

def main():
    cfps = []
    for i in range(1, 29):
        print(f"""===============================================
               page: {i}
===============================================""")
        cfps = cfps + fetchPageCfps(i)

    cpm.cfp_mongo().insert(cfps)

    save_csv(cfps)  # デバッグ用


def fetchPageCfps(page_num):
    return parseHTML(fetchPageData(page_num))

def fetchPageData(page_num):
    data = urlopen("https://fortee.jp/iosdc-japan-2018/proposal?f=all&page={0}".format(page_num))
    response = data.read()
    return response

def parseHTML(rawData):
    rootTree = html.fromstring(rawData)
    cfpsTree  = rootTree.xpath('//div[contains(@class,"list-proposal")]')
    cfps = []
    for cfpTree in cfpsTree:
        cfp = CFP.create(cfpTree) 
        if cfp is not None:
            cfps.append(cfp)
    return cfps

def save_csv(cfps):
    with open('cfps_before.csv', 'w', newline = '', encoding = 'utf-8-sig') as f:
      writer = csv.DictWriter(f,CFP.csvHeader)
      writer.writeheader()
      writer.writerows(map(lambda x: x.generate_document(), cfps))


class CFP:
    def __init__(self):
        self.title = ""
        self.user = ""
        self.talk_type = ""
        self.description = ""
        self.icon_url = ""
        self.twitter_id = ""
        self.detail_url = ""
        self.talk_date = None
        self.talk_site = ""
        self.is_adopted = False 
        self.video_url = ""

    csvHeader = [
        'title',
        'user',
        'talk_type',
        'description',
        'icon_url',
        'twitter_id',
        'detail_url',
        'talk_date',
        'talk_site',
        'is_adopted',
        'video_url'
        ]

    def generate_document(self):
        return {'title': self.title,
                'user': self.user,
                'talk_type': self.talk_type,
                'description': self.description,
                'icon_url': self.icon_url,
                'twitter_id': self.twitter_id,
                'detail_url': self.detail_url,
                'talk_date': self.talk_date,
                'talk_site': self.talk_site,
                'is_adopted': self.is_adopted,
                'video_url': self.video_url
                }

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

【detail_url】
{self.detail_url}

【talk_date】
{self.talk_date}

【talk_site】
{self.talk_site}

【is_adopted】
{self.is_adopted}

【video_url】
{self.video_url}
                """)

    @classmethod
    def create(cls, cfpTree):
        cfp = CFP()
        cfp.title = cfpTree.xpath('./h2/a')[0].text

        cfp.detail_url = 'https://fortee.jp' + cfpTree.xpath('./h2/a')[0].get('href')

        cfp.talk_type = cfpTree.xpath('.//span[contains(@class, "name")]')[0].text

        user_tmp = cfpTree.xpath('.//div[contains(@class,"speaker")]/span')[0].text_content()
        cfp.user = re.sub(r'^(\s|\t|　)+', "", user_tmp)

        description_temp = cfpTree.xpath('./div[contains(@class,"abstract")]')[0].text_content() 
        cfp.description = re.sub(r'^(\s|\t|　)+', "", description_temp)

        # Note:
        # 非公式なプロポーザル（当日のアンカンファレンスなど）は除外する
        if '（概要はありません）' in cfp.description:
            return None

        icon_url_tree = cfpTree.xpath('.//span/img[contains(@class,"inline-avatar")]')
        if len(icon_url_tree) > 0:
            cfp.icon_url = 'https://fortee.jp' + cfpTree.xpath('.//span/img[contains(@class,"inline-avatar")]')[0].get('src')
        else:
            cfp.icon_url = ''

        twitter_urls = cfpTree.xpath('.//span[contains(@class,"left20")]/a')
        if len(twitter_urls) > 0:
            cfp.twitter_id = twitter_urls[0].text 
        else:
            return None

        if len(cfpTree.xpath('.//div[contains(@class,"type")]/span[contains(@class, "tags")]')) > 0:
            cfp.is_adopted = True
            tmp_type_tree = cfpTree.xpath('.//div[contains(@class,"type")]')[0] 
            tmp_schedule = tmp_type_tree.xpath('./span[contains(@class,"schedules")]')[0]
            tmpDate = tmp_schedule.xpath('./span[contains(@class,"schedule")]')[0].text
            cfp.talk_date = datetime.datetime.strptime(tmpDate, '%Y/%m/%d %H:%M〜')
            cfp.talk_site = tmp_schedule.xpath('./span[contains(@class,"track")]')[0].text
            cfp.video_url = cfpTree.xpath('.//ul[contains(@class,"links")]/li[1]/a')[0].attrib['href'] # ビデオ
        cfp.desc()
        return cfp

if __name__ == '__main__':
    main()

