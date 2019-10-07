# coding:utf-8

from driver.Neo4j.connecter import get_connection

from py2neo import Graph
from py2neo import Node
from py2neo import Path
from py2neo import Relationship
from py2neo import RelationshipMatcher


class Neo4jDriver(object):
    table_name = None
    primary_key = None
    id = None

    def __init__(self):
        self.connection = None

    def __del__(self):
        '''
        py2neo未提供close方法， 暂不做处理
        :return:
        '''
        if self.connection is not None:
            pass

    def connector(self):
        if self.connection is None:
            self.connection = get_connection()

    def _check_primary(self, data):
        if self.primary_key is None:
            raise AttributeError("primary key not define")
        if "xid" in data.keys():
            raise ValueError("xid not permit define")
        if self.primary_key == "xid":
            raise AttributeError("primary key not permit is xid")
        if not data[self.primary_key]:
            ValueError("primary key not permit null")

    def _before_insert(self, data):
        return data

    def insert(self, data):
        self._check_primary(data)
        data = self._before_insert(data)
        insert_instance = Node(self.table_name, **data)
        connection = get_connection()
        connection.create(insert_instance)
        return self.queryone(primary_key=self.primary_key)

    def __queryone_meta(self, filter=None):
        '''
        :param filter:
        :return:
        '''
        filter = filter or {}
        connection = get_connection()
        node = connection.nodes.match(self.table_name, **filter).first()
        _result = {}
        if node:
            _result = dict(node)
            _result["xid"] = node.identity

        return _result

    def queryone(self, primary_key, filter=None):
        '''

        :param primary_key:
        :param filter:
        :return:
        '''
        filter = filter or {}
        filter.update({self.primary_key: primary_key})
        _result = self.__queryone_meta(filter)
        return _result

    def __query_meta(self, filter=None, order_by=None, limit=None, skip=None):
        '''
        :param filter:
        :param order_by:  match.order_by("_.name", "max(_.a, _.b)")
        :param limit: number
        :param skip: number
        :return:
        '''
        filter = filter or {}
        connection = get_connection()
        node = connection.nodes.match(self.table_name, **filter)
        if order_by:
            node = node.order_by(order_by)
        if skip:
            node = node.skip(skip)
        if limit:
            node = node.limit(limit)

        _result = []
        for _data in node:
            _tm_data = dict(_data)
            _tm_data["xid"] = _data.identity
            _result.append(_tm_data)

        return _result

    def query(self, filter=None, order_by=None, limit=None, skip=None):
        return self.__query_meta(filter, order_by, limit, skip)

    def __update_meta(self, data, filter=None):
        '''

        :param filter:
        :return:
        '''
        filter = filter or {}
        connection = get_connection()
        node = connection.nodes.match(self.table_name, **filter).first()
        _result = {}
        if node:
            node.update(**data)
            connection.push(node)
            _result = dict(node)
            _result["xid"] = node.identity

        return _result

    def update(self, primary_key, data, filter=None):
        '''
        更新一条数据
        :param primary_key:
        :param data:
        :param filter:
        :return:
        '''
        filter = filter or {}
        filter.update({self.primary_key: primary_key})

        _result = self.__update_meta(data, filter)
        return _result

    def __update_many_meta(self, data, filter=None):
        '''
        py2neo只能一条一条更新， 更新速率可能比较慢
        :param filter:
        :return:
        '''
        filter = filter or {}
        connection = get_connection()
        nodes = connection.nodes.match(self.table_name, **filter)
        _result = []
        for _node in nodes:
            _node.update(**data)
            connection.push(_node)
            _res = dict(_node)
            _res["xid"] = _node.identity
            _result.append(_res)
        return _result

    def update_many(self, filter, data):
        '''
        不允许一次性更新全部数据， 必须加入filter参数
        :param filter:
        :param data:
        :return:
        '''

        return self.__update_many_meta(data, filter)

    def __delete_meta(self, filter=None):
        '''

        :param filter:
        :return:
        '''
        filter = filter or {}
        connection = get_connection()
        node = connection.nodes.match(self.table_name, **filter).first()
        _result = 0
        if node:
            connection.delete(node)
            _result = 1
        return _result

    def delete(self, primary_key, filter=None):
        '''
        删除一条数据
        :param primary_key:
        :param filter:
        :return:
        '''
        filter = filter or {}
        filter.update({self.primary_key: primary_key})

        _result = self.__delete_meta(filter)
        return _result

    def __delete_many_meta(self, filter=None):
        '''
        py2neo只能一条一条删除
        :param filter:
        :return:
        '''
        filter = filter or {}
        connection = get_connection()
        nodes = connection.nodes.match(self.table_name, **filter)
        _result = 0
        for _node in nodes:
            connection.delete(_node)
            _result += 1
        return _result

    def delete_many(self, filter, data):
        '''
        不允许一次性删除全部数据， 必须加入filter参数
        :param filter:
        :param data:
        :return:
        '''

        return self.__delete_many_meta(filter)

    def create_relation(self, primary_key1, primary_key2, re_type, **kwargs):
        '''
        :param primary_key1:
        :param primary_key2:
        :param re_type:
        :param kwargs: 可设置关系键， 用于查找关系
        :return:
        '''
        connection = get_connection()
        key1 = {self.primary_key: primary_key1}
        key2 = {self.primary_key: primary_key2}
        node1 = connection.nodes.match(self.table_name, **key1).first()
        node2 = connection.nodes.match(self.table_name, **key2).first()
        if node1 is None or node2 is None:
            return 0
        s = Relationship(node1, re_type, node2, **kwargs)
        connection.create(s)
        return 1

    def delete_relation(self, filter):
        '''

        :param filter: dict
        :return:
        '''
        connection = get_connection()
        res = connection.relationships.match(**filter).first()
        if res:
            connection.delete(res)
            return 1
        else:
            return 0

    def match_relation(self, primary_key1, primary_key2, re_type=Node):
        _result = []
        connection = get_connection()
        key1 = {self.primary_key: primary_key1}
        key2 = {self.primary_key: primary_key2}
        node1 = connection.nodes.match(self.table_name, **key1).first()
        node2 = connection.nodes.match(self.table_name, **key2).first()
        if node1 is None or node2 is None:
            return _result
        relations = connection.match(nodes=(node1, node2), re_type=re_type)
        for relation in relations:
            retype = re_type or relation.__class__.__name__
            _result.append(retype)

        return _result

    def __fetch_nodes(self, nodes):
        result = []
        for node in nodes:
            _res = dict(node)
            if _res:
                # 跳过关系
                _res["xid"] = node.identity
                result.append(_res)

        return result

    def deep_match_relation(self, primary_key1, primary_key2, deep=None):
        _result = {}
        deep = None or 1
        connection = get_connection()
        key1 = {self.primary_key: primary_key1}
        key2 = {self.primary_key: primary_key2}
        node1 = connection.nodes.match(self.table_name, **key1).first()
        node2 = connection.nodes.match(self.table_name, **key2).first()
        if node1 is None or node2 is None:
            return _result

        n1 = node1.identity
        n2 = node2.identity
        cql = "START d=node(%s), e=node(%s) MATCH p = shortestpath((d)-[*..%s]-(e)) RETURN p" % (n1, n2, deep)
        results = connection.run(cql)
        for res in results:
            _result[str(res[0])] = self.__fetch_nodes(res.to_subgraph().nodes)

        return _result
