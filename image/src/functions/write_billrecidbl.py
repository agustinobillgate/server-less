from functions.additional_functions import *
import decimal
from models import Bill

def write_billrecidbl(t_bill:[T_bill]):
    success_flag = False
    bill = None

    t_bill = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill


        nonlocal t_bill
        nonlocal t_bill_list
        return {"success_flag": success_flag}

    t_bill = query(t_bill_list, first=True)

    if t_bill:

        bill = db_session.query(Bill).filter(
                (Bill._recid == t_Bill.bl_recid)).first()

        if bill:
            buffer_copy(t_bill, bill)

            success_flag = True

    return generate_output()