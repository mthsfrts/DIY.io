import grpc
from concurrent import futures
import time

import config.message_pb2_grpc as servicer
import config.message_pb2 as encryptor


class GrpcServicer:

    def ServerClient(self):
        pass

    def ClientServer(self):
        pass

    def InteractingStream(self):
        pass


def srv():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer.add_GrpcServicer_to_server(GrpcServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    print("Server is Running!")
    server.wait_for_termination()


if __name__ == "__main__":
    srv()
