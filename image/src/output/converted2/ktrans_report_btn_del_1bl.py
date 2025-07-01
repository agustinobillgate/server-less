#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_compli

def ktrans_report_btn_del_1bl(c_list_s_recid:int):
    successflag = False
    h_compli = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, h_compli
        nonlocal c_list_s_recid

        return {"successflag": successflag}


    h_compli = get_cache (H_compli, {"_recid": [(eq, c_list_s_recid)]})

    if h_compli:
        db_session.delete(h_compli)
        successflag = True


    else:
        successflag = False

    return generate_output()