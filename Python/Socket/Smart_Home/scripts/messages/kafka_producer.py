import time
from kafka import KafkaProducer
import pickle as pick


# Serializing data
class Serialize:
    """
    Class responsible for serialize all the messages
    """

    @staticmethod
    def pickle(message):
        """
        Serialization method.

        :return: Binary object
        """
        pickled = pick.dumps(message)

        return pickled


class Kafkaproducer:
    """
    Class responsible for handling Kafka sent messages, to the server
    """

    @staticmethod
    def kafkaSend(sensor_data, topic):
        # Connecting producer to the Kafka Server
        producer = KafkaProducer(bootstrap_servers=["localhost:9092"], value_serializer=Serialize.pickle(sensor_data))

        # Starting send data
        while True:
            msg = sensor_data
            print(sensor_data)
            producer.send(topic, msg)
            time.sleep(5)
