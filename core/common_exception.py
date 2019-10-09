import falcon


class MethodNotAllowed(falcon.HTTPError):
    pass


class ResourceNotFound(falcon.HTTPError):
    pass
