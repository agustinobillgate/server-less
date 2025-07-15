#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def read_billbl(case_type:int, billno:int, resno:int, reslinno:int, actflag:int):
    t_bill_data = []
    bill = None

    t_bill = None

    t_bill_data, T_bill = create_model_like(Bill)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_data, bill
        nonlocal case_type, billno, resno, reslinno, actflag


        nonlocal t_bill
        nonlocal t_bill_data

        return {"t-bill": t_bill_data}

    if case_type == 1:

        bill = get_cache (Bill, {"rechnr": [(eq, billno)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 2:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 3:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.flag == 0)).order_by(Bill._recid).all():
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)

    elif case_type == 4:

        bill = get_cache (Bill, {"rechnr": [(eq, billno)],"flag": [(eq, actflag)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 5:

        bill = get_cache (Bill, {"rechnr2": [(eq, billno)],"rechnr": [(ne, resno)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 6:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"flag": [(eq, 0)],"zinr": [(eq, to_string(actflag))]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 7:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"zinr": [(eq, "")]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 8:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"parent_nr": [(eq, reslinno)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 9:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno)).order_by(Bill._recid).all():
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 10:

        bill = get_cache (Bill, {"rechnr": [(eq, billno)],"resnr": [(eq, resno)],"reslinnr": [(eq, 0)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 11:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"zinr": [(eq, "")],"flag": [(eq, 0)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 12:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"parent_nr": [(eq, reslinno)],"rechnr": [(ne, 0)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 13:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.reslinnr == reslinno) & (Bill.zinr == to_string(actflag))).order_by(Bill._recid).all():
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 14:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"zinr": [(eq, "")]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 15:

        bill = get_cache (Bill, {"resnr": [(eq, resno)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 16:

        bill = get_cache (Bill, {"_recid": [(eq, billno)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 17:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.zinr == to_string(actflag)) & (Bill.flag == 0)).order_by(Bill._recid).all():
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 18:

        for bill in db_session.query(Bill).filter(
                 (Bill.rechnr == billno)).order_by(Bill._recid).all():
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 19:

        bill = get_cache (Bill, {"rechnr": [(eq, billno)],"resnr": [(eq, resno)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 20:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.zinr == to_string(actflag)) & (Bill.flag == 0)).order_by(Bill._recid).all():
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 21:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"flag": [(eq, actflag)]})

        if bill:
            t_bill = T_bill()
            t_bill_data.append(t_bill)

            buffer_copy(bill, t_bill)

    return generate_output()