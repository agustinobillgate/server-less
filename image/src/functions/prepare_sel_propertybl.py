from functions.additional_functions import *
import decimal
from models import Eg_property

def prepare_sel_propertybl(maintask:int):
    t_eg_property_list = []
    eg_property = None

    t_eg_property = None

    t_eg_property_list, T_eg_property = create_model("T_eg_property", {"nr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_property_list, eg_property


        nonlocal t_eg_property
        nonlocal t_eg_property_list
        return {"t-eg-property": t_eg_property_list}

    for eg_property in db_session.query(Eg_property).filter(
            (Eg_property.maintask == maintask)).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        t_eg_property.nr = eg_property.nr
        t_eg_property.bezeich = eg_property.bezeich

    return generate_output()