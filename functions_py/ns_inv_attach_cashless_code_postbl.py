#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Queasy, Bill_line, Guest

def ns_inv_attach_cashless_code_postbl(dept:int, qr_code:string, bill_recid:int):

    prepare_cache ([Bill, Bill_line, Guest])

    ok_flag = False
    msg_int = 0
    temp_list_data = []
    found_sameqr:bool = False
    invalid_code:bool = False
    transaction_exist:bool = False
    bill = queasy = bill_line = guest = None

    b1_list = temp_list = buf_bill = None

    b1_list_data, B1_list = create_model("B1_list", {"resnr":int, "rechnr":int, "name":string, "vorname1":string, "anrede1":string, "saldo":Decimal, "printnr":int, "datum":date, "b_recid":int, "adresse1":string, "wohnort":string, "bemerk":string, "plz":string, "bill_datum":date, "qr_code":string})
    temp_list_data, Temp_list = create_model_like(B1_list)

    Buf_bill = create_buffer("Buf_bill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, msg_int, temp_list_data, found_sameqr, invalid_code, transaction_exist, bill, queasy, bill_line, guest
        nonlocal dept, qr_code, bill_recid
        nonlocal buf_bill


        nonlocal b1_list, temp_list, buf_bill
        nonlocal b1_list_data, temp_list_data

        return {"ok_flag": ok_flag, "msg_int": msg_int, "temp-list": temp_list_data}


    if qr_code == None:
        qr_code = ""

    for buf_bill in db_session.query(Buf_bill).filter(
             (Buf_bill.flag == 0) & (Buf_bill.resnr == 0) & (Buf_bill.reslinnr == 1) & (Buf_bill.rechnr > 0)).order_by(Buf_bill._recid).yield_per(100):

        if buf_bill.vesrdepot2.lower()  != "" and buf_bill.vesrdepot2.lower()  == (qr_code).lower() :
            found_sameqr = True
            break

    if found_sameqr:
        msg_int = 1

        return generate_output()

    if qr_code != "":

        queasy = get_cache (Queasy, {"key": [(eq, 248)],"char2": [(eq, qr_code)]})

        if not queasy:
            invalid_code = True

        if invalid_code:
            msg_int = 2

            return generate_output()

    if qr_code == "" or qr_code == None:

        buf_bill = get_cache (Bill, {"_recid": [(eq, bill_recid)],"flag": [(eq, 0)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"rechnr": [(gt, 0)],"vesrdepot2": [(ne, "")]})

        if buf_bill:

            bill_line = get_cache (Bill_line, {"rechnr": [(eq, buf_bill.rechnr)]})

            if bill_line:
                msg_int = 3

                return generate_output()

    bill = db_session.query(Bill).filter(Bill._recid == bill_recid).with_for_update().first()

    if bill:
        db_session.refresh(bill, with_for_update=True)
        
        bill.vesrdepot2 = qr_code
        temp_list = Temp_list()
        temp_list_data.append(temp_list)

        temp_list.resnr = bill.resnr
        temp_list.rechnr = bill.rechnr
        temp_list.saldo =  to_decimal(bill.saldo)
        temp_list.printnr = bill.printnr
        temp_list.datum = bill.datum
        temp_list.b_recid = bill._recid
        temp_list.qr_code = bill.vesrdepot2

        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

        if guest:
            temp_list.name = guest.name
            temp_list.vorname1 = guest.vorname1
            temp_list.anrede1 = guest.anrede1
            temp_list.adresse1 = guest.adresse1
            temp_list.wohnort = guest.wohnort
            temp_list.bemerk = guest.bemerkung
            temp_list.plz = guest.plz

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)]})

        if bill_line:
            temp_list.bill_datum = bill_line.bill_datum
        pass
        pass
        ok_flag = True

    return generate_output()