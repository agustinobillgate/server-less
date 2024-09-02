from functions.additional_functions import *
import decimal
from models import Eg_property

def eg_property_btn_addartbl():
    nr = 0
    temp_nr:int = 0
    eg_property = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal nr, temp_nr, eg_property


        return {"nr": nr}


    for eg_property in db_session.query(Eg_property).all():

        if temp_nr == 0:
            temp_nr = eg_property.nr
        else:

            if temp_nr < eg_property.nr:
                temp_nr = eg_property.nr
            else:
                temp_nr = temp_nr
    nr = temp_nr + 1

    return generate_output()