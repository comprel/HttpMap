# coding:utf-8

from core.route import Routes

from core.conf import loadsModel
from controller.index import index_route as Index_routes
from controller.urlmap import Routes_Map


def initmap():
    '''
    模块化加载service服务， 默认all， 加载所有
    如需加载指定模块， 则配置指定模块，使用逗号(,) 分隔
    若指定加载的模块不存在，则抛出异常
    :return:
    '''
    ROUTES = []
    if loadsModel == "all":
        for model, modelmap in Routes_Map.items():
            ROUTES.extend(modelmap)
    else:
        for _loadmode in loadsModel:
            try:
                ROUTES.extend(Routes_Map.get(_loadmode))
            except:
                print("模块： %s 不存在或定义异常" % (_loadmode))
    return ROUTES


Routes.append(Index_routes)
Routes.append(initmap())
