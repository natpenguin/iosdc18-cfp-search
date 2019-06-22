#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from lxml import html
import csv
import re
import cfp_persistence_manager as cpm
import datetime
import json

def main():
    cfps = []
    for i in range(1, 25):
        print(f"""===============================================
               page: {i}
===============================================""")
        cfps = cfps + fetchPageCfps(i)
        # cfps = fetchPageCfps(i)
        # # c0 = cfps[0].generate_document()
        # # c1 = cfps[1].generate_document()
        # # cfps = [c0, c1]

        # all = map(lambda x: x.generate_document(), cfps)
        # all = list(all)
        # print("🍎")
        # print(all)
        # print("🍊")
        # print(json.dumps(all))

    cfps2 = map(lambda x: x.generate_document(), cfps)

    s = json.dumps(list(cfps2), ensure_ascii=False)
    print(s)

    with open("proposals.json", 'w') as f:
        f.write(s)

    # savepath = 'sample.json'
    # with open(savepath, 'w') as outfile:

    # save_csv(cfps)  # デバッグ用


def fetchPageCfps(page_num):
    return parseHTML(fetchPageData(page_num))

def fetchPageData(page_num):
    # 🍎 URL を変更
    data = urlopen("https://fortee.jp/iosdc-japan-2019/proposal?f=all&page={0}".format(page_num))
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
        self.slide_url = ""

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
        'video_url',
        'slide_url'
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
                'video_url': self.video_url,
                'slide_url': self.slide_url
                }

    def normalization(self):
        dict = {
            'LT（5分）': 'LT',
            'iOSDCルーキーズLT（5分）': 'LT_R',
            'レギュラートーク（30分）': '15m',
            'レギュラートーク（60分）': '30m',
            '技術パッション共有トーク（60分）': 'iOS' # あとで変えるかも
        }
        self.talk_type = dict[self.talk_type]

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

【slide_url】
{self.slide_url}
                """)

    @classmethod
    def create(cls, cfpTree):
        cfp = CFP()
        cfp.title = cfpTree.xpath('./h2/a')[0].text

        cfp.detail_url = 'https://fortee.jp' + cfpTree.xpath('./h2/a')[0].get('href')

        cfp.talk_type = cfpTree.xpath('.//span[contains(@class, "name")]')[0].text.strip()

        cfp.user = cfpTree.xpath('.//div[contains(@class,"speaker")]/span')[0].text_content().strip()

        cfp.description = cfpTree.xpath('./div[contains(@class,"abstract")]')[0].text_content().strip()

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
            # 動画URL（キャンセルの場合は無い）
            video_url = cfpTree.xpath('.//ul[contains(@class,"links")]/li[1]/a')
            if len(video_url) > 0:
                cfp.video_url = video_url[0].attrib['href']
            # スライドURL（無いケースもある）
            slide_url = cfpTree.xpath('.//ul[contains(@class,"links")]/li[2]/a')
            if len(slide_url) > 0:
                cfp.slide_url = slide_url[0].attrib['href']
        cfp.desc()
        cfp.normalization()
        return cfp

if __name__ == '__main__':
    main()

