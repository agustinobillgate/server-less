#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location

def load_eg_locationbl(case_type:int):
    t_eg_location_list = []
    eg_location = None

    t_eg_location = None

    t_eg_location_list, T_eg_location = create_model_like(Eg_location, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_location_list, eg_location
        nonlocal case_type


        nonlocal t_eg_location
        nonlocal t_eg_location_list

        return {"t-eg-location": t_eg_location_list}

    if case_type == 1:

        for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
            t_eg_location = T_eg_location()
            t_eg_location_list.append(t_eg_location)

            buffer_copy(eg_location, t_eg_location)
            t_eg_location.rec_id = eg_location._recid

    return generate_output()