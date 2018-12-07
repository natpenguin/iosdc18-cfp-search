import unittest
import cfp_scraping as scraping

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


if __name__ == "__main__":
    unittest.main()
