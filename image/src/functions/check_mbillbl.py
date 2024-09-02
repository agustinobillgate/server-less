from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Res_line

def check_mbillbl():
    c_list_list = []
    bill = res_line = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"name":str, "rechnr":int, "saldo":decimal, "zinr":str, "abreise":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, bill, res_line


        nonlocal c_list
        nonlocal c_list_list
        return {"c-list": c_list_list}

    for bill in db_session.query(Bill).filter(
            (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.flag == 0)).all():

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.active_flag <= 1)).first()

        if not res_line:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.resstatus == 8)).first()

            if res_line:
                c_list = C_list()
            c_list_list.append(c_list)

            c_list.rechnr = bill.rechnr
            c_list.name = bill.name
            c_list.saldo = bill.saldo

            if res_line:
                c_list.abreise = res_line.abreise
                c_list.zinr = res_line.zinr

    return generate_output()