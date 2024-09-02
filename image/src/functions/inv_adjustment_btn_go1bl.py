from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def inv_adjustment_btn_go1bl(from_grp:int, mat_grp:int, early_adjust:bool, edit_mode:bool, inv_postdate:date):
    transdate = None
    its_ok:bool = True
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal transdate, its_ok, htparam


        return {"transdate": transdate}


    if from_grp == mat_grp:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        transdate = fdate
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        transdate = fdate

    if early_adjust and inv_postdate < transdate:
        transdate = inv_postdate

    return generate_output()