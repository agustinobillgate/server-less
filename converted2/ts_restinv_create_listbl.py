#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restinv_create_listbl(curr_dept:int, curr_waiter:int):

    prepare_cache ([H_bill])

    table_list_data = []
    h_bill = None

    table_list = hbill = None

    table_list_data, Table_list = create_model("Table_list", {"rechnr":int, "tischnr":int, "saldo":Decimal, "belong":string}, {"belong": "L"})

    Hbill = create_buffer("Hbill",H_bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal table_list_data, h_bill
        nonlocal curr_dept, curr_waiter
        nonlocal hbill


        nonlocal table_list, hbill
        nonlocal table_list_data

        return {"table-list": table_list_data}


    table_list_data.clear()

    for hbill in db_session.query(Hbill).filter(
             (Hbill.departement == curr_dept) & (Hbill.flag == 0) & (Hbill.kellner_nr == curr_waiter)).order_by(Hbill.tischnr).all():
        table_list = Table_list()
        table_list_data.append(table_list)

        table_list.rechnr = hbill.rechnr
        table_list.saldo =  to_decimal(hbill.saldo)
        table_list.tischnr = hbill.tischnr

    return generate_output()