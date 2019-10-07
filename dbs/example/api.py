# coding:utf-8

from lib.uuidlib import allocate_uuid
from driver.databases.mysql import Mysql
from dbs.example.model import ExampleTable


class ExampleApi(Mysql):
    DBModel = ExampleTable
    primary_key = "id"

    def _before_insert(self, data):
        data[self.primary_key] = allocate_uuid()
        return data

if __name__ == '__main__':
    ns = ExampleApi()
    uuid = allocate_uuid()
    data = {"id": uuid, "name": uuid[:12]}
    count, res = ns.insert(data)
    print('create', count, res)
    res2 = ns.get(primiry_id=uuid)
    print('get', res2)

    count, res = ns.update(primiry_id=uuid, data={"task_id": "--------"})
    print('update', count, res)

    # res = ns.delete(primiry_id=uuid)
    # print('delete', res)
