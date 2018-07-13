#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pymongo
import threading
from bson.json_util import dumps

class cfp_mongo:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        print('init')
    def __new__(cls):
            with cls._lock:
                    if cls._instance is None:
                            cls._instance = super().__new__(cls)
                            cls._instance.setup()

            return cls._instance

    def setup(self):
        host = os.getenv("CFP_MONGO_HOST", "localhost")
        port = int(os.getenv("CFP_MONGO_PORT", "27017"))
        # mongodb へのアクセスを確立
        self.client = pymongo.MongoClient(host, port)
        self.database = self.client.iosdc2018_phase_0
        self.collection = self.database.cfps

    def insert(self, cfps):
        self.collection.insert_many(map(lambda x: x.generate_document(), cfps))

    def find_all(self):
        return self.collection.find()

    def get_cfps_json(self):
        return dumps(self.find_all())

mongo = cfp_mongo()

