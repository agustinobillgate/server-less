#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_splitbill_build_rmenubl import ts_splitbill_build_rmenubl
from models import H_bill_line

def ts_splitbill_select_rmenubl(rec_id_h_bill_line:int, rec_id:int, curr_select:int, dept:int):

    prepare_cache ([H_bill_line])

    max_rapos = 0
    temp_data = []
    rhbline_data = []
    h_bill_line = None

    temp = rhbline = None

    temp_data, Temp = create_model("Temp", {"pos":int, "bezeich":string, "artnr":int})
    rhbline_data, Rhbline = create_model("Rhbline", {"nr":int, "rid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_rapos, temp_data, rhbline_data, h_bill_line
        nonlocal rec_id_h_bill_line, rec_id, curr_select, dept


        nonlocal temp, rhbline
        nonlocal temp_data, rhbline_data

        return {"max_rapos": max_rapos, "temp": temp_data, "Rhbline": rhbline_data}


    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, rec_id_h_bill_line)]})
    h_bill_line.waehrungsnr = 0
    pass
    pass
    max_rapos, temp_data, Rhbline_data = get_output(ts_splitbill_build_rmenubl(rec_id, dept, curr_select))

    return generate_output()