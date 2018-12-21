import unittest
import api as api

class TestSummarize(unittest.TestCase):
    def test_summarize_proposals(self):
        datas = [
            {
                "title": "hello",
                "user": "user1",
                "is_adopted": False,
                "talk_type": "30m",
                "detail_url": "http://example.com/0",
            },
            {
                "title": "hello",
                "user": "user1",
                "is_adopted": True,
                "talk_type": "15m",
                "detail_url": "http://example.com/1",
            },
            {
                "title": "goodbye",
                "user": "user3",
                "is_adopted": True,
                "talk_type": "15m",
                "detail_url": "http://example.com/2",
            },
            {
                "title": "goodbye",
                "user": "user3",
                "is_adopted": False,
                "talk_type": "15m",
                "detail_url": "http://example.com/3",
            },
            {
                "title": "hello2",
                "user": "user1",
                "is_adopted": False,
                "talk_type": "30m",
                "detail_url": "http://example.com/4",
            },
            {
                "title": "hello",
                "user": "user2",
                "is_adopted": False,
                "talk_type": "30m",
                "detail_url": "http://example.com/5",
            }
        ]
        datas = api.summarize_proposals(datas)

        self.assertEqual(datas, [
            # title / user が同一のものは集約されること
            {
                "title": "hello",
                "user": "user1",
                "is_adopted": True,
                "talk_types": ["15m", "30m"], # 文字列の昇順でソート
                "detail_url": "http://example.com/1",
            },
            # 同一のトークタイプは集約されること
            {
                "title": "goodbye",
                "user": "user3",
                "is_adopted": True,
                "talk_types": ["15m"],
                "detail_url": "http://example.com/2",
            },
            # title が不一致なものは集約されないこと
            {
                "title": "hello2",
                "user": "user1",
                "is_adopted": False,
                "talk_types": ["30m"],
                "detail_url": "http://example.com/4",
            },
            # user が不一致なものは集約されないこと
            {
                "title": "hello",
                "user": "user2",
                "is_adopted": False,
                "talk_types": ["30m"],
                "detail_url": "http://example.com/5",
            },
        ])


if __name__ == "__main__":
    unittest.main()
