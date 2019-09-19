# coding:utf-8

def url(path, func):
    return {"uri_template": path, "resource": func}


class __Routes(object):
    __routes_map__ = []
    __routes__ = []

    @classmethod
    def __check_handler(cls, func):
        if not func:
            raise ValueError("处理函数不能为空")
        try:
            func.__class__.__name__
        except AttributeError as e:
            raise ValueError("处理函数需为 class类")

    @classmethod
    def __check_url(cls, url):
        if not url:
            raise ValueError("URL PATH 不能为空")
        if not isinstance(url, str):
            print(url)
            raise ValueError("非法URL PATH")
        if not url.startswith("/"):
            raise ValueError("不正确的URL PATH: %s" % url)
        if url not in cls.__routes__:
            cls.__routes__.append(url)

    @classmethod
    def _check_register(cls, path):
        cls.__check_url(path.get("uri_template"))
        cls.__check_handler(path.get("resource"))
        cls.__routes_map__.append(path)

    @classmethod
    def register(cls, url):
        cls._check_register(url)

    @classmethod
    def append(cls, url):
        if not isinstance(url, (dict, list)):
            print(url)
            raise ValueError("注册路由不正确")
        if isinstance(url, dict):
            cls._check_register(url)
        else:
            for _url in url:
                cls._check_register(_url)

    @classmethod
    def urls(cls):
        return cls.__routes_map__


Routes = __Routes
