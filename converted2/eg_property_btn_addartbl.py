#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property

def eg_property_btn_addartbl():

    prepare_cache ([Eg_property])

    nr = 0
    temp_nr:int = 0
    eg_property = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal nr, temp_nr, eg_property

        return {"nr": nr}


    for eg_property in db_session.query(Eg_property).order_by(Eg_property.nr).all():

        if temp_nr == 0:
            temp_nr = eg_property.nr
        else:

            if temp_nr < eg_property.nr:
                temp_nr = eg_property.nr
            else:
                temp_nr = temp_nr
    nr = temp_nr + 1

    return generate_output()