from driver.MQ.Kafka_producer import KafkaProducerClient


def send_access_data(msg):
    return KafkaProducerClient().send(msg)

