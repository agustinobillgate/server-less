from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Res_line, Bill_line

def read_bill1bl(case_type:int, billno:int, resno:int, reslinno:int, actflag:int, roomno:str, datum1:date, datum2:date, saldo1:decimal, saldo2:decimal):
    t_bill_list = []
    bl_saldo:decimal = to_decimal("0.0")
    bill = res_line = bill_line = None

    t_bill = rline = bbuff = tbuff = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})

    Rline = create_buffer("Rline",Res_line)
    Bbuff = create_buffer("Bbuff",Bill)
    Tbuff = create_buffer("Tbuff",Bill)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_list, bl_saldo, bill, res_line, bill_line
        nonlocal case_type, billno, resno, reslinno, actflag, roomno, datum1, datum2, saldo1, saldo2
        nonlocal rline, bbuff, tbuff


        nonlocal t_bill, rline, bbuff, tbuff
        nonlocal t_bill_list
        return {"t-bill": t_bill_list}

    def cr_bill():

        nonlocal t_bill_list, bl_saldo, bill, res_line, bill_line
        nonlocal case_type, billno, resno, reslinno, actflag, roomno, datum1, datum2, saldo1, saldo2
        nonlocal rline, bbuff, tbuff


        nonlocal t_bill, rline, bbuff, tbuff
        nonlocal t_bill_list


        bl_saldo =  to_decimal("0")

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
            bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

        if bl_saldo != bill.saldo:

            tbuff = db_session.query(Tbuff).filter(
                     (Tbuff._recid == bill._recid)).first()
            tbuff.saldo =  to_decimal(bl_saldo)
            pass
        t_bill = T_bill()
        t_bill_list.append(t_bill)

        buffer_copy(bill, t_bill)
        t_bill.bl_recid = bill._recid


    if case_type == 1:

        bill = db_session.query(Bill).filter(
                 (Bill.rechnr == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 2:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.parent_nr != 0) & (Bill.flag == actflag) & (Bill.zinr == roomno)).order_by(Bill._recid).all():
            cr_bill()
    elif case_type == 3:

        bill = db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.billnr == billno) & (Bill.flag == actflag) & (Bill.zinr == roomno)).first()

        if bill:
            cr_bill()
    elif case_type == 4:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.flag == actflag) & (Bill.zinr == roomno)).order_by(Bill._recid).all():
            cr_bill()
    elif case_type == 5:

        bill = db_session.query(Bill).filter(
                 (Bill._recid == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 6:

        bill = db_session.query(Bill).filter(
                 (Bill.flag == actflag) & (Bill.datum >= datum1) & (Bill.datum <= datum2) & (Bill.saldo != 0)).first()

        if bill:
            cr_bill()
    elif case_type == 7:

        bill = db_session.query(Bill).filter(
                 (Bill.flag == actflag) & ((Bill.saldo >= saldo1) | (Bill.saldo <= - saldo2))).first()

        if bill:
            cr_bill()
    elif case_type == 8:

        bill = db_session.query(Bill).filter(
                 (Bill.flag == actflag) & (Bill.vesrdepot == roomno) & (Bill.billtyp == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 9:

        bill = db_session.query(Bill).filter(
                 (Bill.flag == actflag) & (Bill.rechnr == reslinno) & (Bill.resnr == resno) & (Bill.reslinnr == 1) & (Bill.billtyp == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 10 or case_type == 11:

        if actflag == 0:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.zinr == roomno) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                for bill in db_session.query(Bill).filter(
                         (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():

                    if bill.zinr != res_line.zinr:

                        bbuff = db_session.query(Bbuff).filter(
                                 (Bbuff._recid == bill._recid)).first()
                        bbuff.zinr = res_line.zinr


                        pass
                    cr_bill()

        else:

            bill_obj_list = []
            for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr)).filter(
                     (Bill.zinr == roomno) & (Bill.flag == actflag)).order_by(Bill._recid).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                cr_bill()

    elif case_type == 12:

        bill = db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.parent_nr != 0) & (Bill.billnr == billno) & (Bill.flag == actflag) & (Bill.zinr == roomno)).first()

        if bill:
            cr_bill()

    return generate_output()