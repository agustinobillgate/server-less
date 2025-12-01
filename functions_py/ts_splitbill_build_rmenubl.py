#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, H_bill_line, H_artikel

def ts_splitbill_build_rmenubl(rec_id:int, dept:int, curr_select:int):

    prepare_cache ([H_bill, H_bill_line, H_artikel])

    max_rapos = 0
    temp_data = []
    rhbline_data = []
    h_bill = h_bill_line = h_artikel = None

    temp = rhbline = None

    temp_data, Temp = create_model("Temp", {"pos":int, "bezeich":string, "artnr":int})
    rhbline_data, Rhbline = create_model("Rhbline", {"nr":int, "rid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_rapos, temp_data, rhbline_data, h_bill, h_bill_line, h_artikel
        nonlocal rec_id, dept, curr_select


        nonlocal temp, rhbline
        nonlocal temp_data, rhbline_data

        return {"max_rapos": max_rapos, "temp": temp_data, "Rhbline": rhbline_data}

    def build_rmenu():

        nonlocal max_rapos, temp_data, rhbline_data, h_bill, h_bill_line, h_artikel
        nonlocal rec_id, dept, curr_select


        nonlocal temp, rhbline
        nonlocal temp_data, rhbline_data

        curr_rapos:int = 1
        i:int = 0
        temp_data.clear()
        rhbline_data.clear()
        curr_rapos = 1
        max_rapos = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept) & (H_bill_line.waehrungsnr == curr_select)).order_by(H_bill_line.bezeich).all():

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})
            i = i + 1
            temp = Temp()
            temp_data.append(temp)

            temp.pos = i
            temp.artnr = h_bill_line.artnr

            if h_artikel and (h_artikel.artart == 0 or h_artikel.artart == 1):
                temp.bezeich = to_string(h_bill_line.anzahl) + " " + h_bill_line.bezeich
            else:
                temp.bezeich = h_bill_line.bezeich
            rhbline = Rhbline()
            rhbline_data.append(rhbline)

            rhbline.nr = i
            rhbline.rid = h_bill_line._recid
        max_rapos = i

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    build_rmenu()

    return generate_output()