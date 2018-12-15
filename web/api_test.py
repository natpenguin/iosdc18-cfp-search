import unittest
import api as api

class TestSummarize(unittest.TestCase):
    def test_summarize_proposals(self):
        datas = [
            {
                "title": "hello",
                "user": "user1",
                "is_adopted": False,
                "talk_type": "レギュラートーク（15分）",
                "detail_url": "http://example.com/0",
            },
            {
                "title": "hello",
                "user": "user1",
                "is_adopted": True,
                "talk_type": "レギュラートーク（30分）",
                "detail_url": "http://example.com/1",
            },
            {
                "title": "hello2",
                "user": "user1",
                "is_adopted": False,
                "talk_type": "レギュラートーク（30分）",
                "detail_url": "http://example.com/2",
            },
            {
                "title": "hello",
                "user": "user2",
                "is_adopted": False,
                "talk_type": "レギュラートーク（30分）",
                "detail_url": "http://example.com/3",
            }
        ]
        datas = api.summarize_proposals(datas)

        self.assertEqual(datas, [
            # title / user が同一のものは集約されること
            {
                "title": "hello",
                "user": "user1",
                "is_adopted": True,
                "talk_type": "レギュラートーク（15分） / レギュラートーク（30分）",
                "detail_url": "http://example.com/1",
            },
            # title が不一致なものは集約されないこと
            {
                "title": "hello2",
                "user": "user1",
                "is_adopted": False,
                "talk_type": "レギュラートーク（30分）",
                "detail_url": "http://example.com/2",
            },
            # user が不一致なものは集約されないこと
            {
                "title": "hello",
                "user": "user2",
                "is_adopted": False,
                "talk_type": "レギュラートーク（30分）",
                "detail_url": "http://example.com/3",
            },
        ])


if __name__ == "__main__":
    unittest.main()
