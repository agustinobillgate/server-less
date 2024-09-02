from functions.additional_functions import *
import decimal
from models import H_bill, H_bill_line, H_artikel

def ts_splitbill_build_rmenubl(rec_id:int, dept:int, curr_select:int):
    max_rapos = 0
    temp_list = []
    rhbline_list = []
    h_bill = h_bill_line = h_artikel = None

    temp = rhbline = None

    temp_list, Temp = create_model("Temp", {"pos":int, "bezeich":str, "artnr":int})
    rhbline_list, Rhbline = create_model("Rhbline", {"nr":int, "rid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_rapos, temp_list, rhbline_list, h_bill, h_bill_line, h_artikel


        nonlocal temp, rhbline
        nonlocal temp_list, rhbline_list
        return {"max_rapos": max_rapos, "temp": temp_list, "Rhbline": rhbline_list}

    def build_rmenu():

        nonlocal max_rapos, temp_list, rhbline_list, h_bill, h_bill_line, h_artikel


        nonlocal temp, rhbline
        nonlocal temp_list, rhbline_list

        curr_rapos:int = 1
        i:int = 0
        temp_list.clear()
        Rhbline_list.clear()
        curr_rapos = 1
        max_rapos = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == dept) &  (H_bill_line.waehrungsnr == curr_select)).all():

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()
            i = i + 1
            temp = Temp()
            temp_list.append(temp)

            temp.pos = i
            temp.artnr = h_bill_line.artnr

            if h_artikel and (h_artikel.artart == 0 or h_artikel.artart == 1):
                temp.bezeich = to_string(h_bill_line.anzahl) + " " + h_bill_line.bezeich
            else:
                temp.bezeich = h_bill_line.bezeich
            rhbline = Rhbline()
            rhbline_list.append(rhbline)

            Rhbline.nr = i
            Rhbline.rid = h_bill_line._recid
        max_rapos = i


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    build_rmenu()

    return generate_output()