#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_splitbill_build_rmenubl import ts_splitbill_build_rmenubl
from models import H_bill_line

def ts_splitbill_select_rmenubl(rec_id_h_bill_line:int, rec_id:int, curr_select:int, dept:int):

    prepare_cache ([H_bill_line])

    max_rapos = 0
    temp_list = []
    rhbline_list = []
    h_bill_line = None

    temp = rhbline = None

    temp_list, Temp = create_model("Temp", {"pos":int, "bezeich":string, "artnr":int})
    rhbline_list, Rhbline = create_model("Rhbline", {"nr":int, "rid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_rapos, temp_list, rhbline_list, h_bill_line
        nonlocal rec_id_h_bill_line, rec_id, curr_select, dept


        nonlocal temp, rhbline
        nonlocal temp_list, rhbline_list

        return {"max_rapos": max_rapos, "temp": temp_list, "Rhbline": rhbline_list}


    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, rec_id_h_bill_line)]})
    h_bill_line.waehrungsnr = 0
    pass
    pass
    max_rapos, temp_list, Rhbline_list = get_output(ts_splitbill_build_rmenubl(rec_id, dept, curr_select))

    return generate_output()