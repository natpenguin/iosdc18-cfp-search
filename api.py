import falcon
import pymongo

class Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        mongo_response = mongo().collection.find()
        # 要変換処理
        resp.body = (mongo_response)

app = falcon.API()
app.add_route('/', Resource())

# モジュール化したほうがよさそ
class mongo:
    def __init__(self):
        # mongodb へのアクセスを確立
        self.client = pymongo.MongoClient('localhost', 27017)
        self.database = self.client.iosdc2018
        self.collection = self.database.cfps
