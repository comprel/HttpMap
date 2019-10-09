from core.controller import BaseResponse
from dbs.host.api import HostApi
from dbs.host.graphApi import HostGraphApi


class GraphAllHandler(BaseResponse):
    allowed_methods = ["GET"]

    def list(self, req, data, resp, **kwargs):
        re_type = data.pop("re_type", None)
        result = HostGraphApi().match_relation(re_type)
        return len(result), result


class GraphNodeHandler(BaseResponse):
    allowed_methods = ["GET"]

    def detail(self, req, data, resp, **kwargs):
        uuid = kwargs.pop("uuid", None)
        re_type = data.pop("re_type", None)
        HostApi().valitdae_host(uuid)
        result = HostGraphApi().match_node(primary_key1=uuid, re_type=re_type)
        return {"data": result}


class GraphRealtionHandler(BaseResponse):
    allowed_methods = ["GET"]

    def detail(self, req, data, resp, **kwargs):
        '''
        :param req:
        :param data:
        re_type 关系类型
        is_exists 校验是否存在一定的关联关系，做深度搜索，可与max_search_deep结合，限制搜索深度
        max_search_deep 与 is_exists 配合使用，单独使用不生效，默认搜索深度3
        :param resp:
        :param kwargs:
        :return:
        '''
        uuid1 = kwargs.pop("uuid1", None)
        uuid2 = kwargs.pop("uuid2", None)
        re_type = data.pop("re_type", None)
        is_exists = data.pop("is_exists", None)
        max_search_deep = data.pop("max_search_deep", 3)
        HostApi().valitdae_host(uuid1)
        HostApi().valitdae_host(uuid2)
        if is_exists:
            return HostGraphApi().deep_match_relation(primary_key1=uuid1,
                                                      primary_key2=uuid2,
                                                      deep=max_search_deep)
        result = HostGraphApi().match_node_relation(primary_key1=uuid1,
                                                    primary_key2=uuid2,
                                                    re_type=re_type)
        return {"data": result}
