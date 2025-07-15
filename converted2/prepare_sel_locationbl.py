#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location, Queasy

def prepare_sel_locationbl():
    t_eg_location_data = []
    t_queasy_data = []
    eg_location = queasy = None

    t_eg_location = t_queasy = None

    t_eg_location_data, T_eg_location = create_model_like(Eg_location)
    t_queasy_data, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_location_data, t_queasy_data, eg_location, queasy


        nonlocal t_eg_location, t_queasy
        nonlocal t_eg_location_data, t_queasy_data

        return {"t-eg-location": t_eg_location_data, "t-queasy": t_queasy_data}


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 135)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_data.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    return generate_output()