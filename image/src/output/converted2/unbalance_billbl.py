#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Guest, Bill

def unbalance_billbl():

    prepare_cache ([Guest])

    bill_list_list = []
    bill_date:date = None
    res_line = guest = bill = None

    bill_list = None

    bill_list_list, Bill_list = create_model("Bill_list", {"rechnr":int, "resnr":int, "reslinnr":int, "resv_name":string, "gname":string, "ci":string, "co":string, "rmno":string, "balanced":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_list_list, bill_date, res_line, guest, bill


        nonlocal bill_list
        nonlocal bill_list_list

        return {"bill-list": bill_list_list}


    bill_date = get_output(htpdate(110))

    res_line = get_cache (Res_line, {"resstatus": [(eq, 8)],"abreise": [(eq, bill_date)],"l_zuordnung[2]": [(eq, 0)]})
    while None != res_line:

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"parent_nr": [(eq, res_line.reslinnr)],"saldo": [(ne, 0)]})
        while None != bill:
            bill_list = Bill_list()
            bill_list_list.append(bill_list)

            bill_list.rechnr = bill.rechnr
            bill_list.resnr = bill.resnr
            bill_list.reslinnr = bill.parent_nr
            bill_list.resv_name = guest.name
            bill_list.gname = res_line.name
            bill_list.ci = to_string(res_line.ankunft, "99/99/9999")
            bill_list.co = to_string(res_line.abreise, "99/99/9999")
            bill_list.rmno = res_line.zinr
            bill_list.balanced =  to_decimal(bill.saldo)

            curr_recid = bill._recid
            bill = db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.saldo != 0) & (Bill._recid > curr_recid)).first()

        curr_recid = res_line._recid
        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == bill_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line._recid > curr_recid)).first()

    return generate_output()