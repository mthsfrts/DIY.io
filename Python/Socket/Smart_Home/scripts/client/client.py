import grpc
import time
import config.message_pb2_grpc as servicer
import config.message_pb2 as encryptor


def user():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = servicer.GrpcStub(channel)
        print("Hi. I`m PORN - Problematic Object Rather Normal.\n"
              "I am your new home assistant.")
        print("How can I help you?")
        print("Here is your home:")
        print("1 - Air Conditioners\n"
              "2 - Lights\n"
              "3 - Emergency appliances\n"
              "X - To quit")
        device = input("Choose a device to see all the available commands.")
    while True:
        if device == "1":
            print("Here is what I can control on the air conditioner:")

        elif device == "2":
            print("Here is what I can control on the lights:")

        elif device == "3":
            print("Here is what I can control on the emergency appliances:")

        else:
            print("See you soon!")
            break


if __name__ == "__main__":
    user()
