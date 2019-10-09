from pymongo import MongoClient
from core.conf import MONGO_SERVICE
from core.conf import MONGO_DB
from core.conf import MONGO_PORT
from core.conf import MONGO_USER
from core.conf import MONGO_PASSWORD

connect = MongoClient(MONGO_SERVICE, port=MONGO_PORT,
                      username=MONGO_USER,
                      password=MONGO_PASSWORD)


class MongoDb(object):
    collection_name = None

    def __init__(self):
        self.session = None

    def __del__(self):
        '''
        实例销毁，回收session
        :return:
        '''
        if self.session is not None:
            self.session = None

    def get_session(self):
        '''
        分配连接, 返回db
        :return:
        '''
        if self.session is None:
            self.session = connect[MONGO_DB]

    def _before_insert(self, data):
        return data

    def insert(self, data):
        '''
        插入一条数据
        :param data:
        :return:
        '''
        data = self._before_insert(data)
        self.get_session()
        try:
            collection = self.session[self.collection_name]
            _result = collection.insert_one(data)
            return 1, _result.inserted_id
        except Exception as e:
            self.session = None
            raise e

    def _before_insert_many(self, data):
        return data

    def insert_many(self, data):
        '''
        插入多条数据
        :param data:
        :return:
        '''
        data = self._before_insert(data)
        self.get_session()
        try:
            collection = self.session[self.collection_name]
            _result = collection.insert_many(data)
            return len(data), _result.inserted_ids
        except Exception as e:
            self.session = None
            raise e

    def query(self, filter=None, limit=None, offset=None, order_by=None):
        '''
        查询数据列表
        :param filter:
        :param limit: int
        :param offset:
        :param order_by: 如｛"age": -1｝ age倒序
        :return:
        '''
        filter = filter or {}
        self.get_session()
        try:
            collection = self.session[self.collection_name]
            query = collection.find(filter)

            if limit:
                query = query.limit(limit)
            if offset:
                query = query.skip(offset)
            if order_by:
                query = query.sort(order_by)
            result = []
            for q in query:
                result.append(q)

            return len(result), result
        except Exception as e:
            self.session = None
            raise e

    def queryone(self, filter=None):
        '''
        查询数据
        :param filter:
        :return:
        '''
        filter = filter or {}
        self.get_session()
        try:
            collection = self.session[self.collection_name]
            query = collection.find_one(filter)
            return query
        except Exception as e:
            self.session = None
            raise e

    def delete(self, filter=None):
        '''
        删除一条数据
        :param filter:
        :return:
        '''
        filter = filter or {}
        self.get_session()
        try:
            collection = self.session[self.collection_name]
            query = collection.delete_one(filter)
            return query.deleted_count
        except Exception as e:
            self.session = None
            raise e

    def delete_many(self, filter=None):
        '''
        删除多条数据
        :param filter:
        :return:
        '''
        filter = filter or {}
        self.get_session()
        try:
            collection = self.session[self.collection_name]
            query = collection.delete_many(filter)
            return query.deleted_count
        except Exception as e:
            self.session = None
            raise e
