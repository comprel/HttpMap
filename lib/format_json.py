import json
from datetime import date, datetime


def __default(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r not json' % obj)


def to_str(data):
    return json.dumps(data, default=__default)


def to_json(data):
    return json.loads(data)
