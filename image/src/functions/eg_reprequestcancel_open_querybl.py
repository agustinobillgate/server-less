from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_request

def eg_reprequestcancel_open_querybl(fdate:date, tdate:date):
    t_eg_request_list = []
    eg_request = None

    t_eg_request = None

    t_eg_request_list, T_eg_request = create_model_like(Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_request_list, eg_request


        nonlocal t_eg_request
        nonlocal t_eg_request_list
        return {"t-eg-request": t_eg_request_list}

    for eg_request in db_session.query(Eg_request).filter(
            (Eg_request.cancel_date >= fdate) &  (Eg_request.cancel_date <= tdate) &  (Eg_request.delete_flag)).all():
        t_eg_request = T_eg_request()
        t_eg_request_list.append(t_eg_request)

        buffer_copy(eg_request, t_eg_request)

    return generate_output()