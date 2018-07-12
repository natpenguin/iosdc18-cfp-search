import falcon
from cfp_persistence_manager import mongo
from bson.json_util import dumps

class Resource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.get_cfps_json()

    def get_cfps_json(self):
        mongo_response = mongo.find_all()
        return dumps(mongo_response)

class ResourceHealth(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = "OK"

app = falcon.API()
app.add_route('/api', Resource())
app.add_route('/api/health', ResourceHealth())
