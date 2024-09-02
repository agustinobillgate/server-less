from functions.additional_functions import *
import decimal
from models import Eg_property

def eg_property_btn_gobl():
    t_eg_property_list = []
    eg_property = None

    t_eg_property = None

    t_eg_property_list, T_eg_property = create_model_like(Eg_property)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_property_list, eg_property


        nonlocal t_eg_property
        nonlocal t_eg_property_list
        return {"t-eg-property": t_eg_property_list}

    for eg_property in db_session.query(Eg_property).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    return generate_output()