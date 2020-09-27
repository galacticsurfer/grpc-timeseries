import time
from flask import Flask
from flask import request
from flask import jsonify, make_response
from flask_cors import cross_origin
from helper import NiftyForm, NiftyWrapper

app = Flask(__name__)


@app.route('/', methods=['POST'])
@cross_origin()
def nifty_close():
    request_json = request.form.to_dict(flat=True)
    if request_json:
        form = NiftyForm(**request_json)
    else:
        form = NiftyForm(start_date=1,
                         end_date=int(time.time()))
    if form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data
    else:
        return form.errors

    wrapper_obj = NiftyWrapper(port=8010)
    data = wrapper_obj.get_data(start_date=start_date, end_date=end_date)
    return make_response(jsonify(data), 201)



