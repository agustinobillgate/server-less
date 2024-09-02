from functions.additional_functions import *
import decimal
from models import Eg_maintain, Eg_request, Eg_staff

def eg_staff_btn_delartbl(staff_nr:int, rec_id:int):
    fl_code = 0
    eg_maintain = eg_request = eg_staff = None

    egmain = egreq = None

    Egmain = Eg_maintain
    Egreq = Eg_request

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_maintain, eg_request, eg_staff
        nonlocal egmain, egreq


        nonlocal egmain, egreq
        return {"fl_code": fl_code}


    egmain = db_session.query(Egmain).filter(
            (egMain.pic == staff_nr) &  (Egmain.TYPE != 3)).first()

    egreq = db_session.query(Egreq).filter(
            (Egreq.assign_to == staff_nr) &  (Egreq.reqstatus != 5)).first()

    if egMain or egreq:
        fl_code = 1

        return generate_output()

    eg_staff = db_session.query(Eg_staff).filter(
            (Eg_staff._recid == rec_id)).first()

    eg_staff = db_session.query(Eg_staff).first()
    eg_staff.activeflag = False

    fl_code = 2

    return generate_output()