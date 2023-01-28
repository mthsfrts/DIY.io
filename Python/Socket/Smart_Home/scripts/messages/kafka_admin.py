from kafka.admin import KafkaAdminClient, NewTopic

KafkaAdmin = KafkaAdminClient(bootstrap_servers="localhost:9092",
                              client_id="test")


class KafkaAdminClient:

    @staticmethod
    def createTopic(topic, partitions, replication_factor):

        topic_list = []
        topic_list.append(NewTopic(name=topic,
                                   num_partitions=partitions,
                                   replication_factor=replication_factor))
        KafkaAdmin.create_topics(new_topics=topic_list, validate_only=False)




