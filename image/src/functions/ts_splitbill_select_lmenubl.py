from functions.additional_functions import *
import decimal
from functions.ts_splitbill_build_rmenubl import ts_splitbill_build_rmenubl
from models import H_bill_line

def ts_splitbill_select_lmenubl(rec_id_h_bill_line:int, rec_id:int, curr_select:int, dept:int):
    max_rapos = 0
    temp_list = []
    rhbline_list = []
    h_bill_line = None

    temp = rhbline = None

    temp_list, Temp = create_model("Temp", {"pos":int, "bezeich":str, "artnr":int})
    rhbline_list, Rhbline = create_model("Rhbline", {"nr":int, "rid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_rapos, temp_list, rhbline_list, h_bill_line


        nonlocal temp, rhbline
        nonlocal temp_list, rhbline_list
        return {"max_rapos": max_rapos, "temp": temp_list, "Rhbline": rhbline_list}


    h_bill_line = db_session.query(H_bill_line).filter(
            (H_bill_line._recid == rec_id_h_bill_line)).first()
    h_bill_line.waehrungsnr = curr_select

    h_bill_line = db_session.query(H_bill_line).first()

    max_rapos, temp_list, Rhbline_list = get_output(ts_splitbill_build_rmenubl(rec_id, dept, curr_select))

    return generate_output()