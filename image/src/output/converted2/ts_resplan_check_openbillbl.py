#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, Queasy, Htparam, Bill, Bill_line, H_bill_line

def ts_resplan_check_openbillbl(pvilanguage:int, curr_dept:int, curr_date:date, s_recid:int):

    prepare_cache ([H_bill, Queasy, Htparam, Bill, Bill_line, H_bill_line])

    err_flag = False
    msg_str = ""
    check_ok = False
    rec_id = 0
    hbill_no = 0
    lvcarea:string = "ts-restdeposit-pay"
    table_no:int = 0
    pax:int = 0
    gastno:int = 0
    ns_billno:int = 0
    curr_zeit:int = 0
    ft_h:int = 0
    ft_m:int = 0
    from_time:int = 0
    depo_amount:Decimal = to_decimal("0.0")
    nsbill_saldo:Decimal = to_decimal("0.0")
    bill_date:date = None
    rsv_date:date = None
    h_bill = queasy = htparam = bill = bill_line = h_bill_line = None

    t_h_bill = buffq251 = queasy251 = buff_hbill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Buffq251 = create_buffer("Buffq251",Queasy)
    Queasy251 = create_buffer("Queasy251",Queasy)
    Buff_hbill = create_buffer("Buff_hbill",H_bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, msg_str, check_ok, rec_id, hbill_no, lvcarea, table_no, pax, gastno, ns_billno, curr_zeit, ft_h, ft_m, from_time, depo_amount, nsbill_saldo, bill_date, rsv_date, h_bill, queasy, htparam, bill, bill_line, h_bill_line
        nonlocal pvilanguage, curr_dept, curr_date, s_recid
        nonlocal buffq251, queasy251, buff_hbill


        nonlocal t_h_bill, buffq251, queasy251, buff_hbill
        nonlocal t_h_bill_list

        return {"err_flag": err_flag, "msg_str": msg_str, "check_ok": check_ok, "rec_id": rec_id, "hbill_no": hbill_no}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})

    if queasy:
        ns_billno = to_int(queasy.deci2)
        gastno = to_int(entry(2, queasy.char2, "&&"))
        ft_h = to_int(substring(queasy.char1, 0, 2))
        ft_m = to_int(substring(queasy.char1, 2, 2))
        rsv_date = queasy.date1
        depo_amount =  to_decimal(queasy.deci1)
        table_no = queasy.number2

    if ns_billno == 0:
        err_flag = True
        msg_str = translateExtended ("Please posting deposit first for Open the Bill.", lvcarea, "")

        return generate_output()

    bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, gastno)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

    if bill:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
            nsbill_saldo =  to_decimal(nsbill_saldo) + to_decimal(bill_line.betrag)

        if nsbill_saldo != 0:
            err_flag = True
            msg_str = translateExtended ("Nonstay Bill not balance. Open Bill not possible.", lvcarea, "")

            return generate_output()
    from_time = (ft_h * 3600) + ft_m * 60
    curr_zeit = get_current_time_in_seconds()

    if bill_date == rsv_date:

        if curr_zeit < from_time:
            err_flag = True
            msg_str = translateExtended ("Not yet entered the Reservation Time. Open Bill not possible.", lvcarea, "")

            return generate_output()

    elif bill_date < rsv_date:
        err_flag = True
        msg_str = translateExtended ("Not yet entered the Reservation Time. Open Bill not possible.", lvcarea, "")

        return generate_output()

    buffq251 = get_cache (Queasy, {"key": [(eq, 251)],"number2": [(eq, s_recid)]})

    if buffq251:

        buff_hbill = get_cache (H_bill, {"_recid": [(eq, buffq251.number1)]})

        if buff_hbill:

            if buff_hbill.flag == 1:
                err_flag = True
                msg_str = translateExtended ("Bill already closed. Open Bill not possible.", lvcarea, "")

                return generate_output()

    h_bill = get_cache (H_bill, {"flag": [(eq, 0)],"tischnr": [(eq, table_no)],"departement": [(eq, curr_dept)]})

    if h_bill:

        if h_bill.rechnr != 0:

            queasy251 = get_cache (Queasy, {"key": [(eq, 251)],"number1": [(eq, to_int(h_bill._recid))]})

            if queasy251:
                err_flag = True
                msg_str = translateExtended ("Bill already open for this table.", lvcarea, "")

                return generate_output()

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)]})

            if h_bill_line:

                if h_bill_line.bill_datum == rsv_date:
                    rec_id = h_bill._recid
                    hbill_no = h_bill.rechnr
                    msg_str = translateExtended ("Bill already open for this table. Do you want join Deposit to Bill No", lvcarea, "") + " " + to_string(h_bill.rechnr) + " - " + h_bill.bilname + "?" + chr_unicode(10) + "Yes = Join the Bill." + chr_unicode(10) + "No = Create a New Bill and Move Existing Bill."

                    return generate_output()
    check_ok = True

    return generate_output()