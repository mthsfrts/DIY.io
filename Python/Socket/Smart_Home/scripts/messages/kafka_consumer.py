from kafka import KafkaConsumer
import pickle as pick
import time


class deserialize:
    """
    Class responsible for serialize all the messages
    """

    @staticmethod
    def unpickle(message):
        """
        Deserialization method.

        :return: Normal string
        """
        unpickled = pick.loads(message)

        return unpickled


class Kafkaconsumer:

    @staticmethod
    def KafkaReceiving(topic, group):

        # Connecting consumer to the Kafka Server
        consumer = KafkaConsumer(topic=f"topic do kafka server{topic}",
                                 bootstrap_servers=["localhost:9092"],
                                 auto_offset_reset="earliest",
                                 group_id=f"group do kafka {group}")
        print("Starting Consuming.")

        for msg in consumer:
            print(deserialize.unpickle(msg))
            time.sleep(15)

