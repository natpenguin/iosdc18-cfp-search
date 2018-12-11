import unittest
import cfp_scraping as scraping
import HtmlTestRunner

class TestCfpScraping(unittest.TestCase):
    def test_fetchPageCfps(self):
        cfps = scraping.fetchPageCfps(1)
        cfp = cfps[0]
        self.assertEqual(cfp.title, 'リアルタイム革命')
        self.assertTrue(cfp.user)
        self.assertTrue(cfp.talk_type)
        self.assertTrue(cfp.description)
        self.assertTrue(cfp.icon_url)
        self.assertTrue(cfp.twitter_id)
        self.assertTrue(cfp.detail_url)
        self.assertTrue(cfp.talk_date)
        self.assertTrue(cfp.talk_site)
        self.assertTrue(cfp.is_adopted)
        self.assertEqual(cfp.video_url, 'https://www.youtube.com/watch?v=YhBXFaTLXa4')
        self.assertEqual(cfp.slide_url, 'https://speakerdeck.com/keisuke69/the-revolution-of-real-time-webapps')


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='TestCfpScraping'))
