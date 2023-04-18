import logging
from time import sleep
from concurrent import futures

import grpc
import threading

from grpc_health.v1 import health_pb2_grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health

from protos import skynet_pb2_grpc, skynet_pb2
import sydonia_anomisation
import anonimisation


class AuthInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, token):
        self.token = token

    async def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        if "x-api-key" not in metadata:
            return None
        received_token = metadata["x-api-key"]

        if received_token != self.token:
            return None

        return await continuation(handler_call_details)


apiVersion = "1.1.0-beta"
port = "3031"
apiKey = "479b886d-8be9-4aac-bd0b-7ee9025c1ea9"


class SkynetServer(skynet_pb2_grpc.SkynetBlocker):
    """Provides methods that implement functionality of skynet server."""

    def __init__(self) -> None:
        pass

    def Anonimise(self, request: skynet_pb2.AnonimiseRequest,
                  unused_context) -> skynet_pb2.AnonimiseResponse:
        return anonimisation.anonimise(request)

    def SydoniaAnonimiser(self, request: skynet_pb2.SydoniaAnonimiserRequest,
                          unused_context) -> skynet_pb2.SydoniaAnonimiserResponse:
        return sydonia_anomisation.anonimise_sydonia(request)

    def Visualizer(self, request: skynet_pb2.VisualizerRequest,
                   unused_context) -> skynet_pb2.VisualizerRequest:
        return anonimisation.visualize(request)


def _toggle_health(health_servicer: health.HealthServicer, service: str):
    next_status = health_pb2.HealthCheckResponse.SERVING
    while True:
        if next_status == health_pb2.HealthCheckResponse.SERVING:
            next_status = health_pb2.HealthCheckResponse.NOT_SERVING
        else:
            next_status = health_pb2.HealthCheckResponse.SERVING

        health_servicer.set(service, next_status)
        sleep(5)


def _configure_health_server(server: grpc.Server):
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Use a daemon thread to toggle health status
    toggle_health_status_thread = threading.Thread(target=_toggle_health,
                                                   args=(health_servicer,
                                                         "skynet.SkynetBlocker"),
                                                   daemon=True)
    toggle_health_status_thread.start()


# For future use see : https://github.com/grpc-ecosystem/grpc-gateway/issues/1313
def serve():
    health_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    backend = SkynetServer()
    skynet_pb2_grpc.add_SkynetBlockerServicer_to_server(
        backend, server)
    health_server.add_insecure_port('[::]:' + port)
    server.add_insecure_port('[::]:3032')

    _configure_health_server(health_server)
    server.start()
    health_server.start()
    print("Health started, listening on " + port)
    print("Server started, listening on 3032")

    server.wait_for_termination()
    health_server.wait_for_termination()


print("running")

if __name__ == '__main__':
    logging.basicConfig()
    serve()
else:
    serve()
