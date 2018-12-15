import falcon
import pymongo
from functools import reduce
from bson.json_util import dumps

class Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        # TODO: 暫定修正
        client = pymongo.MongoClient(host='mongo', port=27017)
        db = client.iosdc2018_phase_2
        datas = list(db.cfps.find({}, { '_id': False }).sort([("title", pymongo.ASCENDING)]))
        datas = summarize_proposals(datas)
        resp.body = dumps(datas, ensure_ascii=False)
        resp.append_header('Access-Control-Allow-Origin', '*')

        # mongo_response = cpm.cfp_mongo().find_all()
        # # 要変換処理
        # resp.body = (mongo_response)

class ResourceHealth(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = "OK"

def summarize_proposals(datas):
    """
    同一とみなせるプロポーザル（トークタイプが異なる）を集約したリストを返す
    """
    def f(acr, data):
        xs = list(filter(lambda x: is_same_proposal(x, data), acr))
        if len(xs) == 0:
            acr.append(data)
            return acr
        else:
            found = xs[0]
            talk_types = found['talk_type'].split(' / ')
            if data['talk_type'] not in talk_types:
                talk_types.append(data['talk_type'])
                found['talk_type'] = ' / '.join(sorted(talk_types))
            # 採択された方のデータを正とする
            if data.get('is_adopted') == True or data.get('is_adopted_rejectcon') == True or data.get('is_adopted_orecon') == True:
                summarize_proposal(data, found)
            return acr

    return reduce(f, datas, [])

def is_same_proposal(x, y):
    """
    同じプロポーザルと見なすか
    """
    return x['user'] == y['user'] \
        and x['title'] == y['title']

def summarize_proposal(src, dest):
    def copy_if(src, dest, key):
        if key in src:
            dest[key] = src[key]

    copy_if(src, dest, 'is_adopted')
    copy_if(src, dest, 'is_adopted_orecon')
    copy_if(src, dest, 'is_adopted_rejectcon')
    copy_if(src, dest, 'description')
    copy_if(src, dest, 'detail_url')
    copy_if(src, dest, 'video_url')


app = falcon.API()
app.add_route('/api', Resource())
app.add_route('/api/health', ResourceHealth())
