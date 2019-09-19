# coding:utf-8

from falcon import API
from controller.route import Routes


class NetMapAPI(API):
    pass


def makeurl(app, url):
    for _url in url:
        app.add_route(**_url)

    return app


APP = makeurl(NetMapAPI(), Routes.__routes_map__)
