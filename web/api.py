import os, sys
sys.path.append(os.pardir)
from mongo.cfps_data_service import mongo
import falcon

class Resource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  
        resp.body = mongo.get_cfps_json()

class ResourceHealth(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = "OK"

app = falcon.API()
app.add_route('/api', Resource())
app.add_route('/api/health', ResourceHealth())

