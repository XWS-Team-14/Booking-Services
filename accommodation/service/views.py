from proto import test_pb2, test_pb2_grpc


class TestGreeter(test_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return test_pb2.HelloResponse(message=f'Hello, {request.name}!')

    def SayHelloAgain(self, request, context):
        return test_pb2.HelloResponse(message=f'Hello again, {request.name}!')
