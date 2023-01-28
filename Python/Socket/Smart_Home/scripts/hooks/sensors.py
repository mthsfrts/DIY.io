import messages.kafka_producer as kafka


class Sensors:
    """
    :methods: light_sensor, smoke_sensor, temp_sensor
    :major class: Sensors
    :sub classes: luminosity, alarm, thermo
    """

    class luminosity:
        kafka.kafkaSend()
        pass

    class alarm:
        kafka.kafkaSend()
        pass

    class thermo:
        kafka.kafkaSend()
        pass
