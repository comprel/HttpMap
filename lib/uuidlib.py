# coding:utf-8

import uuid


def allocate_uuid():
    _uuid = str(uuid.uuid4())
    _uuid = _uuid.replace("-", "")
    return _uuid.lower()


if __name__ == '__main__':
    print(allocate_uuid())
