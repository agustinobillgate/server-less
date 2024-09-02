from functions.additional_functions import *
import decimal
from models import Eg_maintain, Eg_request

def eg_property_chk_btn_delartbl(property_nr:int):
    fl_code = 0
    eg_maintain = eg_request = None

    egmain = egreq = None

    Egmain = Eg_maintain
    Egreq = Eg_request

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_maintain, eg_request
        nonlocal egmain, egreq


        nonlocal egmain, egreq
        return {"fl_code": fl_code}


    egreq = db_session.query(Egreq).filter(
            (egReq.propertynr == property_nr) &  (egReq.reqstatus != 5)).first()

    egmain = db_session.query(Egmain).filter(
            (Egmain.propertynr == property_nr) &  (Egmain.TYPE != 3)).first()

    if egReq or egmain:

        if egReq.reqstatus != 5 or egmain.TYPE != 3:
            fl_code = 1

            return generate_output()
        else:
            fl_code = 2

            return generate_output()
    else:
        fl_code = 3

        return generate_output()