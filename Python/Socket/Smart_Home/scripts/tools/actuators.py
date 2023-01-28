import messages.kafka_consumer as kafka


class Actuators:
    """
    :methods: Lamp, Detector, Hvac
    :class: Actuators
    """

    class Lamp:
        kafka.Kafkaconsumer()
        pass

    class Detector:
        kafka.Kafkaconsumer()
        pass

    class Hvac:
        kafka.Kafkaconsumer()
        pass
