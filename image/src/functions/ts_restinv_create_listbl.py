from functions.additional_functions import *
import decimal
from models import H_bill

def ts_restinv_create_listbl(curr_dept:int, curr_waiter:int):
    table_list_list = []
    h_bill = None

    table_list = hbill = None

    table_list_list, Table_list = create_model("Table_list", {"rechnr":int, "tischnr":int, "saldo":decimal, "belong":str}, {"belong": "L"})

    Hbill = H_bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal table_list_list, h_bill
        nonlocal hbill


        nonlocal table_list, hbill
        nonlocal table_list_list
        return {"table-list": table_list_list}


    table_list_list.clear()

    for hbill in db_session.query(Hbill).filter(
            (Hbill.departement == curr_dept) &  (Hbill.flag == 0) &  (Hbill.kellner_nr == curr_waiter)).all():
        table_list = Table_list()
        table_list_list.append(table_list)

        table_list.rechnr = hbill.rechnr
        table_list.saldo = hbill.saldo
        table_list.tischnr = hbill.tischnr

    return generate_output()