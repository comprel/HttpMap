from core.controller import BaseResponse
from dbs.example.api import ExampleApi

class Example(BaseResponse):
    allowed_methods = ["GET", "POST"]

    def list(self, req, data, resp, **kwargs):
        # data = {"name": "tom", "age": 18}
        return ExampleApi().query(filter=data, **kwargs)


    def create(self, req, data, resp, **kwargs):
        return ExampleApi().insert(data)
