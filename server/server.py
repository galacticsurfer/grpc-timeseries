from concurrent import futures
import grpc
import timeseries_pb2
import timeseries_pb2_grpc
import pandas as pd


class NiftyService(timeseries_pb2_grpc.NiftyServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""
    def __init__(self, port):
        print("server running on port %d" % (port, ))
        self.port = port
        self.data_frame = pd.read_csv("static/data.csv", low_memory=False)
        self.data_frame['timestamp'] = self.data_frame['Date'].apply(lambda x: int(pd.Timestamp(x).timestamp()))

    def NiftyCall(self, request, context):
        """
        Service method to filter daily close values for Nifty between dates provided in request
        request.startDate:
        request.endDate:
        """
        # Filter the dataframe as per the start and end timestamps
        filtered_df = self.data_frame[(self.data_frame.timestamp > request.startDate) &
                                      (self.data_frame.timestamp < request.endDate)]

        # Iterate through the filtered dataframe and yield the rows
        for _, row in filtered_df.iterrows():
            yield timeseries_pb2.NiftyResponse(date=row['timestamp'], value=row['Close'])


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nifty_service = NiftyService(port=8010)
    timeseries_pb2_grpc.add_NiftyServiceServicer_to_server(nifty_service, server)
    server.add_insecure_port("0.0.0.0:%d" % (nifty_service.port, ))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
