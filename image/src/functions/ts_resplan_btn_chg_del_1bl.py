from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, H_bill, Htparam, H_bill_line, Bill, Bill_line

def ts_resplan_btn_chg_del_1bl(s_recid:int, curr_dept:int, table_no:int):
    flag_code = 0
    deposit_pay = 0
    t_queasy_list = []
    deposit_amt:decimal = 0
    guest_no:int = 0
    ns_billno:int = 0
    depoart:int = 0
    rsv_date:date = None
    queasy = h_bill = htparam = h_bill_line = bill = bill_line = None

    t_queasy = buffq251 = buff_hbill = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"char1":str, "char2":str, "number3":int, "rec_id":int})

    Buffq251 = Queasy
    Buff_hbill = H_bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_code, deposit_pay, t_queasy_list, deposit_amt, guest_no, ns_billno, depoart, rsv_date, queasy, h_bill, htparam, h_bill_line, bill, bill_line
        nonlocal buffq251, buff_hbill


        nonlocal t_queasy, buffq251, buff_hbill
        nonlocal t_queasy_list
        return {"flag_code": flag_code, "deposit_pay": deposit_pay, "t-queasy": t_queasy_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:
        depoart = htparam.finteger

    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == s_recid)).first()
    t_queasy = T_queasy()
    t_queasy_list.append(t_queasy)

    t_queasy.char1 = queasy.char1
    t_queasy.char2 = queasy.char2
    t_queasy.number3 = queasy.number3
    t_queasy.rec_id = queasy._recid


    deposit_amt = queasy.deci1
    guest_no = to_int(entry(2, queasy.char2, "&&"))
    ns_billno = to_int(queasy.deci2)
    rsv_date = queasy.date1

    buffq251 = db_session.query(Buffq251).filter(
            (Buffq251.key == 251) &  (Buffq251.number2 == s_recid)).first()

    if buffq251:

        buff_hbill = db_session.query(Buff_hbill).filter(
                (Buff_hbill._recid == buffq251.number1)).first()

        if buff_hbill:

            if buff_hbill.flag == 1:
                flag_code = 2

                return generate_output()
            else:
                flag_code = 3

                return generate_output()

    h_bill = db_session.query(H_bill).filter(
            (H_bill.flag == 0) &  (H_bill.tischnr == table_no) &  (H_bill.departement == curr_dept)).first()

    if h_bill:

        if h_bill.rechnr != 0:

            h_bill_line = db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).first()

            if h_bill_line:

                if h_bill_line.bill_datum == rsv_date:
                    flag_code = 3

                    return generate_output()

    bill = db_session.query(Bill).filter(
            (Bill.rechnr == ns_billno) &  (Bill.gastnr == guest_no) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (Billtyp == curr_dept) &  (Bill.flag == 1)).first()

    if bill:

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr != depoart)).first()

        if bill_line:
            deposit_pay = bill_line.betrag

    if deposit_amt != 0 and deposit_pay != 0:
        flag_code = 1

        return generate_output()