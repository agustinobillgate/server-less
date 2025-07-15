#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def inv_adjustment_btn_go1bl(from_grp:int, mat_grp:int, early_adjust:bool, edit_mode:bool, inv_postdate:date):

    prepare_cache ([Htparam])

    transdate = None
    its_ok:bool = True
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal transdate, its_ok, htparam
        nonlocal from_grp, mat_grp, early_adjust, edit_mode, inv_postdate

        return {"transdate": transdate}


    if from_grp == mat_grp:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        transdate = htparam.fdate
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        transdate = htparam.fdate

    if early_adjust and inv_postdate < transdate:
        transdate = inv_postdate

    return generate_output()