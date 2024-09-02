from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, H_bill, H_journal, Kellner, Tisch

def ts_oldhbill_btn_exitbl(pvilanguage:int, rechnr:int, curr_dept:int, supervise:bool, bill_date:date, knr:int):
    tischnr = 0
    flag_code = 0
    msg_str = ""
    lvcarea:str = "TS_oldhbill"
    hoteldpt = h_bill = h_journal = kellner = tisch = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tischnr, flag_code, msg_str, lvcarea, hoteldpt, h_bill, h_journal, kellner, tisch


        return {"tischnr": tischnr, "flag_code": flag_code, "msg_str": msg_str}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill.rechnr == rechnr) &  (H_bill.departement == curr_dept) &  (H_bill.flag == 1)).first()

    if not h_bill:
        msg_str = msg_str + chr(2) + translateExtended ("No such closed bill number for POS department", lvcarea, "") + chr(10) + to_string(curr_dept) + " - " + hoteldpt.depart
        flag_code = 1

        return generate_output()

    if not supervise:

        h_journal = db_session.query(H_journal).filter(
                (H_journal.rechnr == rechnr) &  (H_journal.departement == curr_dept) &  (H_journal.bill_datum == bill_date)).first()

        if not h_journal:
            msg_str = msg_str + chr(2) + translateExtended ("The closed bill is older than today", lvcarea, "")
            flag_code = 2

            return generate_output()

        if h_bill.kellner_nr != knr:

            kellner = db_session.query(Kellner).filter(
                    (Kellner_nr == h_bill.kellner_nr)).first()
            msg_str = msg_str + chr(2) + translateExtended ("The bill belongs to other user:", lvcarea, "") + " " + kellnername
            flag_code = 3

            return generate_output()
    tischnr = h_bill.tischnr

    tisch = db_session.query(Tisch).filter(
            (tischnr == tischnr)).first()

    return generate_output()