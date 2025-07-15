#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, Bill, Bill_line, Tisch

def prepare_ts_mkres_1bl(s_recid:int, curr_dept:int):

    prepare_cache ([Htparam, Queasy, Bill, Bill_line, Tisch])

    gname = ""
    telefon = ""
    comments = ""
    gastno = 0
    depo_amount = to_decimal("0.0")
    depo_payment = to_decimal("0.0")
    date_depopay = None
    ns_billno = 0
    active_deposit = False
    t_tisch_data = []
    depoart:int = 0
    htparam = queasy = bill = bill_line = tisch = None

    t_tisch = None

    t_tisch_data, T_tisch = create_model("T_tisch", {"tischnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, telefon, comments, gastno, depo_amount, depo_payment, date_depopay, ns_billno, active_deposit, t_tisch_data, depoart, htparam, queasy, bill, bill_line, tisch
        nonlocal s_recid, curr_dept


        nonlocal t_tisch
        nonlocal t_tisch_data

        return {"gname": gname, "telefon": telefon, "comments": comments, "gastno": gastno, "depo_amount": depo_amount, "depo_payment": depo_payment, "date_depopay": date_depopay, "ns_billno": ns_billno, "active_deposit": active_deposit, "t-tisch": t_tisch_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 588)]})

    if htparam:
        active_deposit = htparam.flogical

    if s_recid != 0:

        queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})

        if queasy:
            gname = entry(0, queasy.char2, "&&")
            gastno = to_int(entry(2, queasy.char2, "&&"))
            telefon = trim(substring(queasy.char1, 9))
            comments = entry(1, queasy.char3, ";")
            depo_amount =  to_decimal(queasy.deci1)
            ns_billno = to_int(queasy.deci2)

            bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, gastno)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

            if bill:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(ne, depoart)]})

                if bill_line:
                    depo_payment =  to_decimal(bill_line.betrag)
                    date_depopay = bill_line.bill_datum

    for tisch in db_session.query(Tisch).filter(
             (Tisch.departement == curr_dept)).order_by(Tisch._recid).all():
        t_tisch = T_tisch()
        t_tisch_data.append(t_tisch)

        t_tisch.tischnr = tisch.tischnr

    return generate_output()