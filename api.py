import falcon
import pymongo
import cfp_persisntence_manager as cpm

class Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        mongo_response = cpm.cfp_mongo().find_all()
        # 要変換処理
        resp.body = (mongo_response)

app = falcon.API()
app.add_route('/', Resource())

