#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request

def eg_reprequestcancel_open_querybl(fdate:date, tdate:date):
    t_eg_request_data = []
    eg_request = None

    t_eg_request = None

    t_eg_request_data, T_eg_request = create_model_like(Eg_request)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_request_data, eg_request
        nonlocal fdate, tdate


        nonlocal t_eg_request
        nonlocal t_eg_request_data

        return {"t-eg-request": t_eg_request_data}

    for eg_request in db_session.query(Eg_request).filter(
             (Eg_request.cancel_date >= fdate) & (Eg_request.cancel_date <= tdate) & (Eg_request.delete_flag)).order_by(Eg_request._recid).all():
        t_eg_request = T_eg_request()
        t_eg_request_data.append(t_eg_request)

        buffer_copy(eg_request, t_eg_request)

    return generate_output()