#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Res_line

def fo_invoice_close_billbl(bil_recid:int, user_init:string, bill_date:date):

    prepare_cache ([Bill, Res_line])

    bill_anzahl:int = 0
    curr_billnr:int = 0
    max_anzahl:int = 0
    bill = res_line = None

    bill1 = None

    Bill1 = create_buffer("Bill1",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_anzahl, curr_billnr, max_anzahl, bill, res_line
        nonlocal bil_recid, user_init, bill_date
        nonlocal bill1


        nonlocal bill1

        return {"bil_recid": bil_recid}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
    bill_anzahl = 0
    curr_billnr = bill.billnr

    for bill1 in db_session.query(Bill1).filter(
             (Bill1.resnr == bill.resnr) & (Bill1.parent_nr == bill.parent_nr) & (Bill1.parent_nr != 0) & (Bill1.flag == 0) & (Bill1.zinr == bill.zinr)).order_by(Bill1._recid).all():
        bill_anzahl = bill_anzahl + 1

    if bill_anzahl != curr_billnr:

        bill1 = get_cache (Bill, {"resnr": [(eq, bill.resnr)],"parent_nr": [(eq, bill.parent_nr)],"billnr": [(eq, bill_anzahl)],"flag": [(eq, 0)],"zinr": [(eq, bill.zinr)]})
        bill1.billnr = curr_billnr
        pass
    max_anzahl = bill_anzahl + 1

    if max_anzahl < 5:
        max_anzahl = 5

    for bill1 in db_session.query(Bill1).filter(
             (Bill1.resnr == bill.resnr) & (Bill1.parent_nr == bill.parent_nr) & (Bill1.parent_nr != 0) & (Bill1.flag == 1) & (Bill1.zinr == bill.zinr)).order_by(Bill1._recid).all():
        max_anzahl = max_anzahl + 1
    pass
    bill.billnr = max_anzahl
    bill.flag = 1
    bill.vesrcod = user_init
    pass

    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)],"zinr": [(eq, bill.zinr)]})
    res_line.abreise = bill_date
    res_line.abreisezeit = get_current_time_in_seconds()
    res_line.changed = get_current_date()
    res_line.changed_id = user_init
    res_line.active_flag = 2
    pass

    bill1 = get_cache (Bill, {"resnr": [(eq, bill.resnr)],"parent_nr": [(eq, bill.parent_nr)],"billnr": [(eq, 1)],"flag": [(eq, 0)],"zinr": [(eq, bill.zinr)]})
    bil_recid = bill1._recid

    return generate_output()