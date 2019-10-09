from core.controller import BaseResponse
from dbs.access.mongoApi import AccessMongoApi


class AccessHistoryHandler(BaseResponse):
    allowed_methods = ["GET"]

    def list(self, req, data, resp, **kwargs):
        # mongodb与mysql orm查询排序用法不一致， 需转换
        order_by = kwargs.pop("order_by", None)
        if order_by:
            if order_by.startswith("-"):
                order_by = {order_by: -1}
            else:
                order_by = {order_by: 1}
        return AccessMongoApi().query(filter=data, order_by=order_by, **kwargs)
