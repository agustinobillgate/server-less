from functions.additional_functions import *
import decimal
from models import Bill, Res_line

def write_bill2bl(t_bill:[T_bill]):
    success_flag = False
    bill = res_line = None

    t_bill = None

    t_bill_list, T_bill = create_model_like(Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill, res_line


        nonlocal t_bill
        nonlocal t_bill_list
        return {"success_flag": success_flag}

    t_bill = query(t_bill_list, first=True)

    if t_bill:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == t_Bill.rechnr)).first()

        if not bill:
            bill = Bill()
        db_session.add(bill)

        buffer_copy(t_bill, bill)
        success_flag = True

        if bill.reslinnr != bill.parent_nr:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

            if res_line and res_line.resstatus == 12 and res_line.zinr != bill.zinr:

                res_line = db_session.query(Res_line).first()
                res_line.zinr = bill.zinr

                res_line = db_session.query(Res_line).first()

        bill = db_session.query(Bill).first()

    return generate_output()