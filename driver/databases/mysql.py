# coding:utf-8

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.conf import MYSQL_SERVICE

# 连接数据库
connect = create_engine(MYSQL_SERVICE, encoding="utf-8", pool_pre_ping=True,
                        pool_size=5, pool_timeout=5, max_overflow=10)

Base = declarative_base()


class Mysql(object):
    DBModel = None
    primary_key = "id"

    def __init__(self):
        self.session = None

    def __del__(self):
        '''
        实例销毁，回收session
        :return:
        '''
        if self.session is not None:
            self.session.close()

    def get_session(self):
        '''
        分配连接
        :return:
        '''
        if self.session is None:
            Session = sessionmaker(bind=connect)
            self.session = Session()

    def _validate_model(self):
        if self.DBModel is None:
            raise AttributeError("not define")

    def _validate_prikey(self, data):
        if self.primary_key not in dat.keys():
            raise ValueError("没有主键")

    def _before_insert(self, data):
        return data

    def insert(self, data):
        '''
        插入一条数据
        :param data:
        :return:
        '''
        data = self._before_insert(data)
        _insertInstance = self.DBModel(**data)
        self.get_session()
        try:
            self.session.add(_insertInstance)
            self.session.commit()
            return 1, data[self.primary_key]
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def query(self, filter=None, limit=None, offset=None, order_by=None):
        '''
        查询数据列表
        :param filter:
        :param limit: 默认只返回100条数据
        :param offset:
        :param order_by:
        :return:
        '''
        filter = filter or {}
        self.get_session()
        query = self.session.query(self.DBModel)
        query = query.filter_by(**filter)
        count_sql = query
        limit = limit or 100
        if order_by:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit=limit)
        if offset:
            query = query.offset(offset)

        try:
            count = count_sql.count()
            res = query.all()
            result = []
            for q in res:
                result.append(q.to_json())

            return count, result
        finally:
            self.session.close()

    def __query_meta(self, filter=None, limit=None, offset=None, order_by=None):
        '''
        查询数据列表
        :param filter:
        :param limit:
        :param offset:
        :param order_by:
        :return:
        '''
        filter = filter or {}
        self.get_session()
        query = self.session.query(self.DBModel)
        query = query.filter_by(**filter)
        if order_by:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit=limit)
        if offset:
            query = query.offset(offset)

        try:
            res = query.all()
            result = []
            for q in res:
                result.append(q.to_json())

            return result
        finally:
            self.session.close()

    def count(self, filter=None):
        '''
        统计数据
        :param filter:
        :return:
        '''
        filter = filter or {}
        self.get_session()
        query = self.session.query(self.DBModel)
        query = query.filter_by(**filter)
        count_sql = query
        try:
            count = count_sql.count()
            return count
        finally:
            self.session.close()

    def queryone(self, filter=None):
        '''
        提供查询一条数据
        :param filter:
        :return:
        '''
        filter = filter or {}
        self.get_session()
        query = self.session.query(self.DBModel)
        query = query.filter_by(**filter)

        try:
            res = query.one_or_none()
            if res:
                return res.to_json()
            else:
                return {}

        finally:
            self.session.close()

    def get(self, primiry_id, filter=None):
        '''
        依据主键获取data
        :param primiry_id:
        :param filter:
        :return:
        '''
        data = {self.primary_key: primiry_id}
        filter = filter or {}
        data.update(filter)
        return self.queryone(data)

    def __delete_meta(self, filter=None):
        '''
        提供删除基础功能， 一般不做直接使用
        :param filter:
        :return:
        '''
        filter = filter or {}
        origin_data = self.__query_meta(filter)
        if not origin_data:
            return []

        self.get_session()
        query = self.session.query(self.DBModel)
        query = query.filter_by(**filter)

        try:
            t = query.delete()
            self.session.commit()
            return origin_data
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def _before_delete(self, data):
        return data

    def delete(self, primiry_id, filter=None):
        '''
        依据主键删除数据
        :param primiry_id:
        :param filter:
        :return:
        '''
        data = {self.primary_key: primiry_id}
        filter = filter or {}
        data.update(filter)
        data = self._before_delete(data)
        res = self.__delete_meta(filter=data)
        if res:
            return res[0]
        else:
            return {}

    def _before_delete_many(self, data):
        return data

    def delete_many(self, filter):
        '''
        删除多个数据
        :param filter:  dict
        :return:
        '''
        if not filter:
            raise ValueError("不允许删除全部数据")
        filter = self._before_delete_many(filter)
        return self.__delete_meta(filter)

    def __update_meta(self, data, filter=None):
        '''
        提供更新多行功能
        :param data:
        :param filter:
        :return:
        '''
        filter = filter or {}
        origin_data = self.__query_meta(filter=filter)
        if not origin_data:
            return 0, []
        self.get_session()
        query = self.session.query(self.DBModel)
        query = query.filter_by(**filter)

        try:
            t = query.update(data)
            self.session.commit()
            result = []
            for _data in origin_data:
                result.append(_data.update(data))
            return len(result), result
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def update_many(self, data, filter):
        '''
        更新操作， 不允许更新全部数据
        :param primiry_id:
        :param data:
        :param filter:
        :return:
        '''
        if not filter:
            raise ValueError("不允许更新全部数据")
        return self.__update_meta(data, filter)

    def _before_update(self, data):
        return data

    def update(self, primiry_id, data, filter=None):
        '''
        更新操作
        :param primiry_id:
        :param data:
        :param filter:
        :return:
        '''
        if primiry_id in data.keys():
            raise ValueError("不允许更新主键")
        filter = filter or {}
        filter.update({self.primary_key: primiry_id})
        origin_data = self.queryone(filter)
        if not origin_data:
            return 0, {}
        data = self._before_update(data)
        self.get_session()
        query = self.session.query(self.DBModel)
        query = query.filter_by(**filter)

        try:
            t = query.update(data)
            self.session.commit()
            origin_data.update(data)
            return 1, origin_data
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()


class ModelDict(object):
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

