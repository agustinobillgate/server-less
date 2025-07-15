#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_maintain, Eg_request

def eg_property_chk_btn_delartbl(property_nr:int):

    prepare_cache ([Eg_maintain, Eg_request])

    fl_code = 0
    eg_maintain = eg_request = None

    egmain = egreq = None

    Egmain = create_buffer("Egmain",Eg_maintain)
    Egreq = create_buffer("Egreq",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_maintain, eg_request
        nonlocal property_nr
        nonlocal egmain, egreq


        nonlocal egmain, egreq

        return {"fl_code": fl_code}


    egreq = get_cache (Eg_request, {"propertynr": [(eq, property_nr)],"reqstatus": [(ne, 5)]})

    egmain = get_cache (Eg_maintain, {"propertynr": [(eq, property_nr)],"type": [(ne, 3)]})

    if egreq or egmain:

        if egreq.reqstatus != 5 or egmain.type != 3:
            fl_code = 1

            return generate_output()
        else:
            fl_code = 2

            return generate_output()
    else:
        fl_code = 3

        return generate_output()

    return generate_output()