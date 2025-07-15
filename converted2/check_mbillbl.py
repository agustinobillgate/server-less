#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Res_line

def check_mbillbl():

    prepare_cache ([Bill, Res_line])

    c_list_data = []
    bill = res_line = None

    c_list = None

    c_list_data, C_list = create_model("C_list", {"name":string, "rechnr":int, "saldo":Decimal, "zinr":string, "abreise":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_data, bill, res_line


        nonlocal c_list
        nonlocal c_list_data

        return {"c-list": c_list_data}

    for bill in db_session.query(Bill).filter(
             (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.flag == 0)).order_by(Bill.saldo.desc(), Bill.name).all():

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"active_flag": [(le, 1)]})

        if not res_line:

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})
            pass

            if res_line:
                pass
            c_list = C_list()
            c_list_data.append(c_list)

            c_list.rechnr = bill.rechnr
            c_list.name = bill.name
            c_list.saldo =  to_decimal(bill.saldo)

            if res_line:
                c_list.abreise = res_line.abreise
                c_list.zinr = res_line.zinr

    return generate_output()