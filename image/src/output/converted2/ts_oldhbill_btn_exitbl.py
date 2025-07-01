#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_bill, H_journal, Kellner, Tisch

def ts_oldhbill_btn_exitbl(pvilanguage:int, rechnr:int, curr_dept:int, supervise:bool, bill_date:date, knr:int):

    prepare_cache ([Hoteldpt, H_bill, Kellner])

    tischnr = 0
    flag_code = 0
    msg_str = ""
    lvcarea:string = "TS-oldhbill"
    hoteldpt = h_bill = h_journal = kellner = tisch = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tischnr, flag_code, msg_str, lvcarea, hoteldpt, h_bill, h_journal, kellner, tisch
        nonlocal pvilanguage, rechnr, curr_dept, supervise, bill_date, knr

        return {"tischnr": tischnr, "flag_code": flag_code, "msg_str": msg_str}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    h_bill = get_cache (H_bill, {"rechnr": [(eq, rechnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 1)]})

    if not h_bill:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("No such closed bill number for POS department", lvcarea, "") + chr_unicode(10) + to_string(curr_dept) + " - " + hoteldpt.depart
        flag_code = 1

        return generate_output()

    if not supervise:

        h_journal = get_cache (H_journal, {"rechnr": [(eq, rechnr)],"departement": [(eq, curr_dept)],"bill_datum": [(eq, bill_date)]})

        if not h_journal:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("The closed bill is older than today", lvcarea, "")
            flag_code = 2

            return generate_output()

        if h_bill.kellner_nr != knr:

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)]})
            msg_str = msg_str + chr_unicode(2) + translateExtended ("The bill belongs to other user:", lvcarea, "") + " " + kellner.kellnername
            flag_code = 3

            return generate_output()
    tischnr = h_bill.tischnr

    tisch = get_cache (Tisch, {"tischnr": [(eq, tischnr)]})

    return generate_output()