from driver.Mongodb.mongo import MongoDb


class AccessMongoApi(MongoDb):
    collection_name = "http_access"

