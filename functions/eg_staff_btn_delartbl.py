#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_maintain, Eg_request, Eg_staff

def eg_staff_btn_delartbl(staff_nr:int, rec_id:int):

    prepare_cache ([Eg_staff])

    fl_code = 0
    eg_maintain = eg_request = eg_staff = None

    egmain = egreq = None

    Egmain = create_buffer("Egmain",Eg_maintain)
    Egreq = create_buffer("Egreq",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_maintain, eg_request, eg_staff
        nonlocal staff_nr, rec_id
        nonlocal egmain, egreq


        nonlocal egmain, egreq

        return {"fl_code": fl_code}


    egmain = db_session.query(Egmain).filter(
             (Egmain.pic == staff_nr) & (Egmain.type != 3)).first()

    egreq = db_session.query(Egreq).filter(
             (Egreq.assign_to == staff_nr) & (Egreq.reqstatus != 5)).first()

    if egmain or egreq:
        fl_code = 1

        return generate_output()

    eg_staff = get_cache (Eg_staff, {"_recid": [(eq, rec_id)]})

    if eg_staff:
        pass
        eg_staff.activeflag = False


        pass
        pass
        fl_code = 2

    return generate_output()