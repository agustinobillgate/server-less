from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bill, Queasy, Bill_line, Guest

def ns_inv_attach_cashless_code_postbl(dept:int, qr_code:str, bill_recid:int):
    ok_flag = False
    msg_int = 0
    temp_list_list = []
    found_sameqr:bool = False
    invalid_code:bool = False
    transaction_exist:bool = False
    bill = queasy = bill_line = guest = None

    b1_list = temp_list = buf_bill = None

    b1_list_list, B1_list = create_model("B1_list", {"resnr":int, "rechnr":int, "name":str, "vorname1":str, "anrede1":str, "saldo":decimal, "printnr":int, "datum":date, "b_recid":int, "adresse1":str, "wohnort":str, "bemerk":str, "plz":str, "bill_datum":date, "qr_code":str})
    temp_list_list, Temp_list = create_model_like(B1_list)

    Buf_bill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, msg_int, temp_list_list, found_sameqr, invalid_code, transaction_exist, bill, queasy, bill_line, guest
        nonlocal buf_bill


        nonlocal b1_list, temp_list, buf_bill
        nonlocal b1_list_list, temp_list_list
        return {"ok_flag": ok_flag, "msg_int": msg_int, "temp-list": temp_list_list}


    if qr_code == None:
        qr_code = ""

    for buf_bill in db_session.query(Buf_bill).filter(
            (Buf_bill.flag == 0) &  (Buf_bill.resnr == 0) &  (Buf_bill.reslinnr == 1) &  (Buf_bill.rechnr > 0)).all():

        if buf_bill.vesrdepot2.lower()  != "" and buf_bill.vesrdepot2.lower()  == (qr_code).lower() :
            found_sameqr = True
            break

    if found_sameqr:
        msg_int = 1

        return generate_output()

    if qr_code != "":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 248) &  (func.lower(Queasy.char2) == (qr_code).lower())).first()

        if not queasy:
            invalid_code = True

        if invalid_code:
            msg_int = 2

            return generate_output()

    if qr_code == "" or qr_code == None:

        buf_bill = db_session.query(Buf_bill).filter(
                (Buf_bill._recid == bill_recid) &  (Buf_bill.flag == 0) &  (Buf_bill.resnr == 0) &  (Buf_bill.reslinnr == 1) &  (Buf_bill.rechnr > 0) &  (Buf_bill.vesrdepot2 != "")).first()

        if buf_bill:

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == buf_bill.rechnr)).first()

            if bill_line:
                msg_int = 3

                return generate_output()

    bill = db_session.query(Bill).filter(
            (Bill._recid == bill_recid)).first()

    if bill:

        bill = db_session.query(Bill).first()
        bill.vesrdepot2 = qr_code
        temp_list = Temp_list()
        temp_list_list.append(temp_list)

        temp_list.resnr = bill.resnr
        temp_list.rechnr = bill.rechnr
        temp_list.saldo = bill.saldo
        temp_list.printnr = bill.printnr
        temp_list.datum = bill.datum
        temp_list.b_recid = bill._recid
        temp_list.qr_code = bill.vesrdepot2

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bill.gastnr)).first()

        if guest:
            temp_list.name = guest.name
            temp_list.vorname1 = guest.vorname1
            temp_list.anrede1 = guest.anrede1
            temp_list.adresse1 = guest.adresse1
            temp_list.wohnort = guest.wohnort
            temp_list.bemerk = guest.bemerk
            temp_list.plz = guest.plz

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill.rechnr)).first()

        if bill_line:
            temp_list.bill_datum = bill_line.bill_datum

        bill = db_session.query(Bill).first()

        ok_flag = True

    return generate_output()