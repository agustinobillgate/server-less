#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, H_bill_line, Kellner

def test_webdevbl(from_date:date, to_date:date):

    prepare_cache ([H_bill, H_bill_line, Kellner])

    outlet_transaction_data = []
    curr_dept:int = 1
    waiter:string = ""
    h_bill = h_bill_line = kellner = None

    outlet_transaction = None

    outlet_transaction_data, Outlet_transaction = create_model("Outlet_transaction", {"trans_date":date, "department":int, "waiter_name":string, "table_no":int, "bill_no":int, "guest_name":string, "pax":int, "total_amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outlet_transaction_data, curr_dept, waiter, h_bill, h_bill_line, kellner
        nonlocal from_date, to_date


        nonlocal outlet_transaction
        nonlocal outlet_transaction_data

        return {"outlet-transaction": outlet_transaction_data}

    for h_bill in db_session.query(H_bill).filter(
             (H_bill.saldo != 0) & (H_bill.departement == curr_dept)).order_by(H_bill.rechnr).all():

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(ge, from_date),(le, to_date)],"departement": [(eq, curr_dept)]})

        if h_bill_line:

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)]})

            if kellner:
                waiter = kellner.kellnername
            outlet_transaction = Outlet_transaction()
            outlet_transaction_data.append(outlet_transaction)

            outlet_transaction.trans_date = h_bill_line.bill_datum
            outlet_transaction.department = curr_dept
            outlet_transaction.waiter_name = waiter
            outlet_transaction.table_no = h_bill.tischnr
            outlet_transaction.bill_no = h_bill.rechnr
            outlet_transaction.guest_name = h_bill.bilname
            outlet_transaction.pax = h_bill.belegung
            outlet_transaction.total_amount =  to_decimal(h_bill.saldo)

    return generate_output()