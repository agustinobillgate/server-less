#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from models import H_bill

def tada_post_payment_getsaldobl(rechnr:int, dept:int):
    amount = to_decimal("0.0")
    h_bill = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, h_bill
        nonlocal rechnr, dept


        nonlocal t_h_bill
        nonlocal t_h_bill_list

        return {"amount": amount}

    for h_bill in db_session.query(H_bill).filter(
             (H_bill.rechnr == rechnr) & (H_bill.departement == dept)).order_by(H_bill._recid).all():
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)

    t_h_bill = query(t_h_bill_list, first=True)

    if t_h_bill:
        amount =  to_decimal(t_h_bill.saldo)

    return generate_output()