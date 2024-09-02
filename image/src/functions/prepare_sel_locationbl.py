from functions.additional_functions import *
import decimal
from models import Eg_location, Queasy

def prepare_sel_locationbl():
    t_eg_location_list = []
    t_queasy_list = []
    eg_location = queasy = None

    t_eg_location = t_queasy = None

    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_location_list, t_queasy_list, eg_location, queasy


        nonlocal t_eg_location, t_queasy
        nonlocal t_eg_location_list, t_queasy_list
        return {"t-eg-location": t_eg_location_list, "t-queasy": t_queasy_list}


    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 135)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for eg_location in db_session.query(Eg_location).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    return generate_output()