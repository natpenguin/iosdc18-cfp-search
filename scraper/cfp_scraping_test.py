import unittest
import cfp_scraping as scraping
import HtmlTestRunner
import datetime

class TestCfpScraping(unittest.TestCase):
    def test_fetchPageCfps(self):
        cfps = scraping.fetchPageCfps(1)
        cfp = cfps[0]
        self.assertEqual(cfp.title, 'リアルタイム革命')
        self.assertEqual(cfp.user, '西谷圭介')
        self.assertEqual(cfp.talk_type, 'レギュラートーク（30分）')
        self.assertEqual(cfp.description, 'チャットに代表されるリアルタイムなアプリケーションを皆さんはどのように開発していますか？リアルタイムな双方向通信をサポートするソリューションを利用したり、Socket.ioなどを用いてWebSocketで自前で構築するなどあると思います。本セッションでは新たなクエリ言語として注目されるGraphQLのSubscriptionを用いる方法をGraphQLのマネージドサービスであるAWS AppSyncとあわせてご紹介します。')
        self.assertEqual(cfp.icon_url, 'https://fortee.jp/files/iosdc-japan-2018/speaker/a671c733-f784-4e63-847d-6688a7521f62.jpeg')
        self.assertEqual(cfp.twitter_id, 'Keisuke69')
        self.assertEqual(cfp.detail_url, 'https://fortee.jp/iosdc-japan-2018/proposal/bbf8946d-7c83-4997-ba83-6c65042e41c3')
        self.assertEqual(cfp.talk_date, datetime.datetime(2018, 8, 31, 11, 20))
        self.assertEqual(cfp.talk_site, 'Track C')
        self.assertTrue(cfp.is_adopted)
        self.assertEqual(cfp.video_url, 'https://www.youtube.com/watch?v=YhBXFaTLXa4')
        self.assertEqual(cfp.slide_url, 'https://speakerdeck.com/keisuke69/the-revolution-of-real-time-webapps')


class TestCFP(unittest.TestCase):
    def test_normalization(self):
        cfp = scraping.CFP()
        cfp.talk_type = 'レギュラートーク（30分）'
        cfp.normalization()
        self.assertEqual(cfp.talk_type, '30m')


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='TestCfpScraping'))
