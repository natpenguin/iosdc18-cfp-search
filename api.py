import falcon
import pymongo
import cfp_persistence_manager as cpm

class Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        mongo_response = cpm.cfp_mongo().find_all()
        # 要変換処理
        resp.body = (mongo_response)

class ResourceHealth(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = "OK"

app = falcon.API()
app.add_route('/api', Resource())
app.add_route('/api/health', ResourceHealth())
