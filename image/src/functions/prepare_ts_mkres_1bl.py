from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Queasy, Bill, Bill_line, Tisch

def prepare_ts_mkres_1bl(s_recid:int, curr_dept:int):
    gname = ""
    telefon = ""
    comments = ""
    gastno = 0
    depo_amount = 0
    depo_payment = 0
    date_depopay = None
    ns_billno = 0
    active_deposit = False
    t_tisch_list = []
    depoart:int = 0
    htparam = queasy = bill = bill_line = tisch = None

    t_tisch = None

    t_tisch_list, T_tisch = create_model("T_tisch", {"tischnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, telefon, comments, gastno, depo_amount, depo_payment, date_depopay, ns_billno, active_deposit, t_tisch_list, depoart, htparam, queasy, bill, bill_line, tisch


        nonlocal t_tisch
        nonlocal t_tisch_list
        return {"gname": gname, "telefon": telefon, "comments": comments, "gastno": gastno, "depo_amount": depo_amount, "depo_payment": depo_payment, "date_depopay": date_depopay, "ns_billno": ns_billno, "active_deposit": active_deposit, "t-tisch": t_tisch_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:
        depoart = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 588)).first()

    if htparam:
        active_deposit = htparam.flogical

    if s_recid != 0:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == s_recid)).first()

        if queasy:
            gname = entry(0, queasy.char2, "&&")
            gastno = to_int(entry(2, queasy.char2, "&&"))
            telefon = trim(substring(queasy.char1, 9))
            comments = entry(1, queasy.char3, ";")
            depo_amount = queasy.deci1
            ns_billno = to_int(queasy.deci2)

            bill = db_session.query(Bill).filter(
                    (Bill.rechnr == ns_billno) &  (Bill.gastnr == gastno) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (Billtyp == curr_dept) &  (Bill.flag == 1)).first()

            if bill:

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr != depoart)).first()

                if bill_line:
                    depo_payment = bill_line.betrag
                    date_depopay = bill_line.bill_datum

    for tisch in db_session.query(Tisch).filter(
            (Tisch.departement == curr_dept)).all():
        t_tisch = T_tisch()
        t_tisch_list.append(t_tisch)

        t_tischnr = tischnr

    return generate_output()