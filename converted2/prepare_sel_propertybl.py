#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property

def prepare_sel_propertybl(maintask:int):

    prepare_cache ([Eg_property])

    t_eg_property_data = []
    eg_property = None

    t_eg_property = None

    t_eg_property_data, T_eg_property = create_model("T_eg_property", {"nr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_property_data, eg_property
        nonlocal maintask


        nonlocal t_eg_property
        nonlocal t_eg_property_data

        return {"t-eg-property": t_eg_property_data}

    for eg_property in db_session.query(Eg_property).filter(
             (Eg_property.maintask == maintask)).order_by(Eg_property.nr).all():
        t_eg_property = T_eg_property()
        t_eg_property_data.append(t_eg_property)

        t_eg_property.nr = eg_property.nr
        t_eg_property.bezeich = eg_property.bezeich

    return generate_output()