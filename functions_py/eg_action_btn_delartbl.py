#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_mdetail, Eg_action

def eg_action_btn_delartbl(actionnr:int, rec_id:int):
    fl_code = 0
    eg_mdetail = eg_action = None

    egreq = None

    Egreq = create_buffer("Egreq",Eg_mdetail)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_mdetail, eg_action
        nonlocal actionnr, rec_id
        nonlocal egreq


        nonlocal egreq

        return {"fl_code": fl_code}


    egreq = db_session.query(Egreq).filter(
             (Egreq.key == 1) & (Egreq.nr == actionnr)).first()

    if egreq:
        fl_code = 1

        return generate_output()

    # eg_action = get_cache (Eg_action, {"_recid": [(eq, rec_id)]})
    eg_action = db_session.query(Eg_action).filter(
             (Eg_action._recid == rec_id)).with_for_update().first()

    if eg_action:
        pass
        db_session.delete(eg_action)
        db_session.refresh(eg_action,with_for_update=True)

    return generate_output()
