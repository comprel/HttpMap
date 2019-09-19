from core.route import url

class Index(object):
    def on_get(self, req, resp, **kwargs):
        resp.body = "WELCOME ... "


index_route = url("/", Index())

