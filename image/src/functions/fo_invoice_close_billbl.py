from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Res_line

def fo_invoice_close_billbl(bil_recid:int, user_init:str, bill_date:date):
    bill_anzahl:int = 0
    curr_billnr:int = 0
    max_anzahl:int = 0
    bill = res_line = None

    bill1 = None

    Bill1 = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_anzahl, curr_billnr, max_anzahl, bill, res_line
        nonlocal bill1


        nonlocal bill1
        return {}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()
    bill_anzahl = 0
    curr_billnr = billnr

    for bill1 in db_session.query(Bill1).filter(
            (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.parent_nr != 0) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).all():
        bill_anzahl = bill_anzahl + 1

    if bill_anzahl != curr_billnr:

        bill1 = db_session.query(Bill1).filter(
                (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.billnr == bill_anzahl) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).first()
        bill1.billnr = curr_billnr

        bill1 = db_session.query(Bill1).first()
    max_anzahl = bill_anzahl + 1

    if max_anzahl < 5:
        max_anzahl = 5

    for bill1 in db_session.query(Bill1).filter(
            (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.parent_nr != 0) &  (Bill1.flag == 1) &  (Bill1.zinr == bill.zinr)).all():
        max_anzahl = max_anzahl + 1

    bill = db_session.query(Bill).first()
    billnr = max_anzahl
    bill.flag = 1
    bill.vesrcod = user_init

    bill = db_session.query(Bill).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr) &  (Res_line.zinr == bill.zinr)).first()
    res_line.abreise = bill_date
    res_line.abreisezeit = get_current_time_in_seconds()
    res_line.changed = get_current_date()
    res_line.changed_id = user_init
    res_line.active_flag = 2

    res_line = db_session.query(Res_line).first()

    bill1 = db_session.query(Bill1).filter(
            (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.billnr == 1) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).first()
    bil_recid = bill1._recid

    return generate_output()