from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Guest, Bill

def unbalance_billbl():
    bill_list_list = []
    bill_date:date = None
    res_line = guest = bill = None

    bill_list = None

    bill_list_list, Bill_list = create_model("Bill_list", {"rechnr":int, "resnr":int, "reslinnr":int, "resv_name":str, "gname":str, "ci":str, "co":str, "rmno":str, "balanced":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_list_list, bill_date, res_line, guest, bill


        nonlocal bill_list
        nonlocal bill_list_list
        return {"bill-list": bill_list_list}


    bill_date = get_output(htpdate(110))

    res_line = db_session.query(Res_line).filter(
            (Res_line.resstatus == 8) &  (Res_line.abreise == bill_date) &  (Res_line.l_zuordnung[2] == 0)).first()
    while None != res_line:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnr)).first()

        bill = db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.saldo != 0)).first()
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
            bill_list.balanced = bill.saldo

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.saldo != 0)).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 8) &  (Res_line.abreise == bill_date) &  (Res_line.l_zuordnung[2] == 0)).first()

    return generate_output()