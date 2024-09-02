from functions.additional_functions import *
import decimal
from models import Bill

def read_billbl(case_type:int, billno:int, resno:int, reslinno:int, actflag:int):
    t_bill_list = []
    bill = None

    t_bill = None

    t_bill_list, T_bill = create_model_like(Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_list, bill


        nonlocal t_bill
        nonlocal t_bill_list
        return {"t-bill": t_bill_list}

    if case_type == 1:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == billno)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 2:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.reslinnr == reslinno)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 3:

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno) &  (Bill.flag == 0)).all():
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)

    elif case_type == 4:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == billno) &  (Bill.flag == actflag)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 5:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr2 == billno) &  (Bill.rechnr != resno)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 6:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.reslinnr == reslinno) &  (Bill.flag == 0) &  (Bill.zinr == to_string(actflag))).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 7:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.zinr == "")).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 8:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 9:

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno)).all():
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 10:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == billno) &  (Bill.resnr == resno) &  (Bill.reslinnr == 0)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 11:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.zinr == "") &  (Bill.flag == 0)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 12:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno) &  (Bill.rechnr != 0)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 13:

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.reslinnr == reslinno) &  (Bill.zinr == to_string(actflag))).all():
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 14:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.reslinnr == reslinno) &  (Bill.zinr == "")).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 15:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 16:

        bill = db_session.query(Bill).filter(
                (Bill._recid == billno)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 17:

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno) &  (Bill.zinr == to_string(actflag)) &  (Bill.flag == 0)).all():
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 18:

        for bill in db_session.query(Bill).filter(
                (Bill.rechnr == billno)).all():
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 19:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == billno) &  (Bill.resnr == resno)).first()

        if bill:
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)
    elif case_type == 20:

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.zinr == to_string(actflag)) &  (Bill.flag == 0)).all():
            t_bill = T_bill()
            t_bill_list.append(t_bill)

            buffer_copy(bill, t_bill)

    return generate_output()