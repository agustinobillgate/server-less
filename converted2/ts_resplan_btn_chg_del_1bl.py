#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, H_bill, Htparam, H_bill_line, Bill, Bill_line

def ts_resplan_btn_chg_del_1bl(s_recid:int, curr_dept:int, table_no:int):

    prepare_cache ([Queasy, H_bill, Htparam, H_bill_line, Bill, Bill_line])

    flag_code = 0
    deposit_pay = to_decimal("0.0")
    t_queasy_data = []
    deposit_amt:Decimal = to_decimal("0.0")
    guest_no:int = 0
    ns_billno:int = 0
    depoart:int = 0
    rsv_date:date = None
    queasy = h_bill = htparam = h_bill_line = bill = bill_line = None

    t_queasy = buffq251 = queasy251 = buff_hbill = None

    t_queasy_data, T_queasy = create_model("T_queasy", {"char1":string, "char2":string, "number3":int, "rec_id":int})

    Buffq251 = create_buffer("Buffq251",Queasy)
    Queasy251 = create_buffer("Queasy251",Queasy)
    Buff_hbill = create_buffer("Buff_hbill",H_bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_code, deposit_pay, t_queasy_data, deposit_amt, guest_no, ns_billno, depoart, rsv_date, queasy, h_bill, htparam, h_bill_line, bill, bill_line
        nonlocal s_recid, curr_dept, table_no
        nonlocal buffq251, queasy251, buff_hbill


        nonlocal t_queasy, buffq251, queasy251, buff_hbill
        nonlocal t_queasy_data

        return {"flag_code": flag_code, "deposit_pay": deposit_pay, "t-queasy": t_queasy_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart = htparam.finteger

    queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})
    t_queasy = T_queasy()
    t_queasy_data.append(t_queasy)

    t_queasy.char1 = queasy.char1
    t_queasy.char2 = queasy.char2
    t_queasy.number3 = queasy.number3
    t_queasy.rec_id = queasy._recid


    deposit_amt =  to_decimal(queasy.deci1)
    guest_no = to_int(entry(2, queasy.char2, "&&"))
    ns_billno = to_int(queasy.deci2)
    rsv_date = queasy.date1

    buffq251 = get_cache (Queasy, {"key": [(eq, 251)],"number2": [(eq, s_recid)]})

    if buffq251:

        buff_hbill = get_cache (H_bill, {"_recid": [(eq, buffq251.number1)]})

        if buff_hbill:

            if buff_hbill.flag == 1:
                flag_code = 2

                return generate_output()
            else:
                flag_code = 3

                return generate_output()

    h_bill = get_cache (H_bill, {"flag": [(eq, 0)],"tischnr": [(eq, table_no)],"departement": [(eq, curr_dept)]})

    if h_bill:

        queasy251 = get_cache (Queasy, {"key": [(eq, 251)],"number1": [(eq, to_int(h_bill._recid))],"number2": [(eq, s_recid)]})

        if queasy251:

            if h_bill.rechnr != 0:

                h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)]})

                if h_bill_line:

                    if h_bill_line.bill_datum == rsv_date:
                        flag_code = 3

                        return generate_output()

    bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, guest_no)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

    if bill:

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(ne, depoart)]})

        if bill_line:
            deposit_pay =  to_decimal(bill_line.betrag)

    if deposit_amt != 0 and deposit_pay != 0:
        flag_code = 1

        return generate_output()

    return generate_output()