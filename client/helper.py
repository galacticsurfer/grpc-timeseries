# gRPC Related imports
import grpc
import timeseries_pb2
import timeseries_pb2_grpc
from wtforms import Form, IntegerField, validators


# Form to handle input data
class NiftyForm(Form):
    start_date = IntegerField(u'start_date', [validators.required()])
    end_date = IntegerField(u'end_date', [validators.required()])


class NiftyWrapper(object):
    def __init__(self, port):
        self.port = port

    def get_data(self, start_date, end_date):
        channel = grpc.insecure_channel('0.0.0.0:%d' % (self.port, ))
        stub = timeseries_pb2_grpc.NiftyServiceStub(channel)
        grpc_request = timeseries_pb2.NiftyRequest(startDate=start_date, endDate=end_date)
        result_generator = stub.NiftyCall(grpc_request, wait_for_ready=True)

        data = list()
        for response in result_generator:
            data.append({"ts": response.date, "value": response.value})

        return data
