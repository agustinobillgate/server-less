from functions.additional_functions import *
import decimal
from models import Eg_mdetail, Eg_action

def eg_action_btn_delartbl(actionnr:int, rec_id:int):
    fl_code = 0
    eg_mdetail = eg_action = None

    egreq = None

    Egreq = Eg_mdetail

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_mdetail, eg_action
        nonlocal egreq


        nonlocal egreq
        return {"fl_code": fl_code}


    egreq = db_session.query(Egreq).filter(
            (egReq.key == 1) &  (egReq.nr == actionnr)).first()

    if egReq:
        fl_code = 1

        return generate_output()

    eg_action = db_session.query(Eg_action).filter(
            (Eg_action._recid == rec_id)).first()

    eg_action = db_session.query(Eg_action).first()
    db_session.delete(eg_action)


    return generate_output()