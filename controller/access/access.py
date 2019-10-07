from core.controller import BaseResponse
from tasks.taskClient import send_access_data


class AccessHandler(BaseResponse):
    allowed_methods = ["POST"]

    def validate_null(self, type, resource):
        if not resource:
            raise ValueError("%s 不能为空" % type)

    def create(self, req, data, resp, **kwargs):
        self.validate_null("id", data.get("id"))
        self.validate_null("src", data.get("src"))
        self.validate_null("dest", data.get("dest"))
        self.validate_null("port", data.get("port"))
        cid = send_access_data(data)
        return 1, cid
