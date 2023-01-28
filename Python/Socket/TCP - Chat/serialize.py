import pickle as pick


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

    @staticmethod
    def unpickle(message):
        """
        Deserialization method.

        :return: Normal string
        """
        unpickled = pick.loads(message)

        return unpickled
