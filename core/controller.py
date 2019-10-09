import json
import falcon
import traceback
from lib.logs import logger
from lib.format_json import to_str
from lib.uuidlib import allocate_uuid
from core.conf import LOG_MSG_MAX_LEN
from core.common_exception import MethodNotAllowed
from core.common_exception import ResourceNotFound

header = {"Content-Type": "application/json"}


class _Base(object):
    allowed_methods = ['']

    def __init__(self):
        self.header = None
        self.url = None
        self.req_id = None

    def _validate_method(self, req, **kwargs):
        if req.method.upper() not in self.allowed_methods:
            raise falcon.HTTPMethodNotAllowed(allowed_methods=self.allowed_methods, headers=header,
                                              title="method error", description="method not allowed",
                                              code=405)

    def _validate_header(self, req, **kwargs):
        if req.headers.get("CONTENT-TYPE") != "application/json":
            raise falcon.HTTPError(status=falcon.HTTP_400, title="data error",
                                   description="请求数据需为json", code=400, headers=header)
        self.header = req.headers

    def _fetch_data(self, req, **kwargs):
        try:
            return req.params or {}
        except:
            raise falcon.HTTPError(status=falcon.HTTP_400, title="data error",
                                   description="请求数据需为json", code=400, headers=header)

    def trace_req_log(self, req, data, **kwargs):
        self.req_id = "req-%s" % (allocate_uuid())
        msg = "[ %s ][URL:%s] - [METHOD: %s] [000] - [DATA: %s]" % (self.req_id, req.path,
                                                                    req.method.lower(),
                                                                    to_str(data)[:LOG_MSG_MAX_LEN])
        logger.info(msg)

    def trace_resp_log(self, req, result, resp, **kwargs):
        status = resp.status or 000
        msg = "[ %s ][URL:%s] - [METHOD: %s] [%s] - [RESULT: %s]" % (self.req_id, req.path,
                                                                     req.method.lower(), status,
                                                                     to_str(result)[:LOG_MSG_MAX_LEN])
        logger.info(msg)


class BaseResponse(_Base):
    allowed_methods = ['']

    def _before_list(self, req, data, **kwargs):
        pass

    def list(self, req, data, resp, **kwargs):
        raise MethodNotAllowed(status=falcon.HTTP_405, title="not define")

    def _before_detail(self, req, data, **kwargs):
        pass

    def detail(self, req, data, resp, **kwargs):
        raise MethodNotAllowed(status=falcon.HTTP_405, title="not define")

    def _before_create(self, req, data, **kwargs):
        pass

    def create(self, req, data, resp, **kwargs):
        raise MethodNotAllowed(status=falcon.HTTP_405, title="not define")

    def _before_update(self, req, data, **kwargs):
        pass

    def update(self, req, data, resp, **kwargs):
        raise MethodNotAllowed(status=falcon.HTTP_405, title="not define")

    def _before_delete(self, req, data, **kwargs):
        pass

    def delete(self, req, data, resp, **kwargs):
        raise MethodNotAllowed(status=falcon.HTTP_405, title="not define")

    def __build_filter(self, data):
        pass

    def on_get(self, req, resp, **kwargs):
        '''
        Handles get requests
        :param req:
        :param resp:
        :param kwargs:
        :return: 返回json
        '''
        self.url = req.path
        self._validate_method(req)
        self._validate_header(req)
        data = self._fetch_data(req)
        self.trace_req_log(req, data)
        result = {}
        try:
            if kwargs:
                self._before_detail(req, data, **kwargs)
                result = self.detail(req, data, resp, **kwargs)
            else:
                order_by = data.pop("order_by", None)
                if order_by:
                    if order_by.endswith("__-1"):
                        order_by = "-%s" % order_by.strip("__-1")
                    if order_by.endswith("__1"):
                        order_by = order_by.strip("__1")
                limit = data.pop("limit", None)
                offset = data.pop("offset", None)
                self._before_list(req, data=data)
                count, _data = self.list(req, data, resp, offset=offset, limit=limit, order_by=order_by)
                result = {"count": count, "data": _data}

            if result:
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except (ValueError, TypeError, IndexError, UnicodeError) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_400
            result = {"title": e.__class__.__name__, "description": e.args[0], "code": 400}
        except (ResourceNotFound) as e:
            resp.status = falcon.HTTP_404
        except (MethodNotAllowed) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_405
            result = {"title": "method error", "description": "method not allowed", "code": 405}
        except Exception as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_500
            result = {"title": "service error", "description": "服务器异常", "code": 500}
        finally:
            resp.body = to_str(result)
            resp.set_headers(header)
            resp.set_header("ReqId", self.req_id)
            self.trace_resp_log(req, result=result, resp=resp)

    def on_post(self, req, resp, **kwargs):
        '''
        Handles post requests
        :param req:
        :param resp:
        :param kwargs:
        :return: 返回json
        '''

        self.url = req.path
        self._validate_method(req)
        self._validate_header(req)
        data = self._fetch_data(req)
        self.trace_req_log(req, data)
        result = {}
        try:
            self._before_create(req, data=data, **kwargs)
            num, cid = self.create(req=req, data=data, resp=resp, **kwargs)
            result = {"num": num, "id": cid}
            resp.status = falcon.HTTP_201
        except (ValueError, TypeError, IndexError, UnicodeError) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_400
            result = {"title": e.__class__.__name__, "description": e.args[0], "code": 400}
        except (ResourceNotFound) as e:
            resp.status = falcon.HTTP_404
        except (MethodNotAllowed) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_405
            result = {"title": "method error", "description": "method not allowed", "code": 405}
        except Exception as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_500
            result = {"title": "service error", "description": "服务器异常", "code": 500}
        finally:
            resp.body = to_str(result)
            resp.set_headers(header)
            resp.set_header("ReqId", self.req_id)
            self.trace_resp_log(req, result=result, resp=resp)

    def on_patch(self, req, resp, **kwargs):
        '''
        Handles patch requests
        :param req:
        :param resp:
        :param kwargs:
        :return: 返回json
        '''

        self.url = req.path
        self._validate_method(req)
        self._validate_header(req)
        data = self._fetch_data(req)
        self.trace_req_log(req, data)
        result = {}
        try:
            self._before_update(req, data=data, **kwargs)
            num, update_data = self.update(req=req, data=data, resp=resp, **kwargs)
            if update_data:
                result = {"num": num, "id": update_data}
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except (ValueError, TypeError, IndexError, UnicodeError) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_400
            result = {"title": e.__class__.__name__, "description": e.args[0], "code": 400}
        except (ResourceNotFound) as e:
            resp.status = falcon.HTTP_404
        except (MethodNotAllowed) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_405
            result = {"title": "method error", "description": "method not allowed", "code": 405}
        except Exception as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_500
            result = {"title": "service error", "description": "服务器异常", "code": 500}
        finally:
            resp.body = to_str(result)
            resp.set_headers(header)
            resp.set_header("ReqId", self.req_id)
            self.trace_resp_log(req, result=result, resp=resp)

    def on_put(self, req, resp, **kwargs):
        '''
        Handles put requests
        :param req:
        :param resp:
        :param kwargs:
        :return: 返回json
        '''
        return self.on_patch(req, resp)

    def on_delete(self, req, resp, **kwargs):
        '''
        Handles delete requests
        :param req:
        :param resp:
        :param kwargs:
        :return: 返回json
        '''

        self.url = req.path
        self._validate_method(req)
        self._validate_header(req)
        data = self._fetch_data(req)
        self.trace_req_log(req, data)
        result = {}
        try:
            self._before_delete(req, data=data, **kwargs)
            result = self.delete(req=req, data=data, resp=resp, **kwargs)
            if result:
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except (ValueError, TypeError, IndexError, UnicodeError) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_400
            result = {"title": e.__class__.__name__, "description": e.args[0], "code": 400}
        except (ResourceNotFound) as e:
            resp.status = falcon.HTTP_404
        except (MethodNotAllowed) as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_405
            result = {"title": "method error", "description": "method not allowed", "code": 405}
        except Exception as e:
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_500
            result = {"title": "service error", "description": "服务器异常", "code": 500}
        finally:
            resp.body = to_str(result)
            resp.set_headers(header)
            resp.set_header("ReqId", self.req_id)
            self.trace_resp_log(req, result=result, resp=resp)
