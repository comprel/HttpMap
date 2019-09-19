from core.controller import BaseResponse


class Example(BaseResponse):
    allowed_methods = ["GET", "POST"]

    def list(self, req, data, resp, **kwargs):
        data = {"name": "tom", "age": 18}
        return data

