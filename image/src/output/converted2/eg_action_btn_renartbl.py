#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_mdetail

def eg_action_btn_renartbl(action_actionnr:int):
    avail_req = False
    eg_mdetail = None

    req = None

    Req = create_buffer("Req",Eg_mdetail)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_req, eg_mdetail
        nonlocal action_actionnr
        nonlocal req


        nonlocal req

        return {"avail_req": avail_req}


    req = db_session.query(Req).filter(
             (Req.key == 1) & (Req.nr == action_actionnr)).first()

    if req:
        avail_req = True

    return generate_output()