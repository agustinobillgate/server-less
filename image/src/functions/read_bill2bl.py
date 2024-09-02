from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import Bill, Res_line, Bill_line, Nebenst, Bk_veran, Bk_reser

def read_bill2bl(case_type:int, billno:int, resno:int, reslinno:int, actflag:int, roomno:str, datum1:date, datum2:date, saldo1:decimal, saldo2:decimal):
    telbill_flag = False
    babill_flag = False
    t_bill_list = []
    ba_dept:int = 0
    bill_date:date = None
    bl_saldo:decimal = 0
    bill = res_line = bill_line = nebenst = bk_veran = bk_reser = None

    t_bill = tbuff = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})

    Tbuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal telbill_flag, babill_flag, t_bill_list, ba_dept, bill_date, bl_saldo, bill, res_line, bill_line, nebenst, bk_veran, bk_reser
        nonlocal tbuff


        nonlocal t_bill, tbuff
        nonlocal t_bill_list
        return {"telbill_flag": telbill_flag, "babill_flag": babill_flag, "t-bill": t_bill_list}

    def cr_bill():

        nonlocal telbill_flag, babill_flag, t_bill_list, ba_dept, bill_date, bl_saldo, bill, res_line, bill_line, nebenst, bk_veran, bk_reser
        nonlocal tbuff


        nonlocal t_bill, tbuff
        nonlocal t_bill_list


        bl_saldo = 0

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill.rechnr)).all():
            bl_saldo = bl_saldo + bill_line.betrag

        if bl_saldo != bill.saldo:

            tbuff = db_session.query(Tbuff).filter(
                    (Tbuff._recid == bill._recid)).first()
            tbuff.saldo = bl_saldo

            tbuff = db_session.query(Tbuff).first()

        t_bill = T_bill()
        t_bill_list.append(t_bill)

        buffer_copy(bill, t_bill)
        t_bill.bl_recid = bill._recid

        if bill.rechnr > 0:

            nebenst = db_session.query(Nebenst).filter(
                    (Nebenst.zinr == "") &  (Nebenst.rechnr == bill.rechnr)).first()
            telbill_flag = None != nebenst

            if ba_dept > 0 and billtyp == ba_dept:
                check_banquet()

    def check_banquet():

        nonlocal telbill_flag, babill_flag, t_bill_list, ba_dept, bill_date, bl_saldo, bill, res_line, bill_line, nebenst, bk_veran, bk_reser
        nonlocal tbuff


        nonlocal t_bill, tbuff
        nonlocal t_bill_list

        bk_veran = db_session.query(Bk_veran).filter(
                (Bk_veran.rechnr == bill.rechnr)).first()

        if bk_veran and bk_veran.activeflag == 0:

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.datum > bill_date) &  (Bk_reser.resstatus <= 3)).first()

            if bk_reser:
                babill_flag = True

                return

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.datum == bill_date) &  (Bk_reser.resstatus == 1) &  ((Bk_reser.bis_i * 1800) > get_current_time_in_seconds())).first()

            if bk_reser:
                babill_flag = True

                return


    bill_date = get_output(htpdate(110))
    ba_dept = get_output(htpint(900))

    if ba_dept == 0:
        ba_dept = -1

    if case_type == 1:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 2:

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno) &  (Bill.parent_nr != 0) &  (Bill.flag == actflag) &  (Bill.zinr == roomno)).all():
            cr_bill()
    elif case_type == 3:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno) &  (Billnr == billno) &  (Bill.flag == actflag) &  (Bill.zinr == roomno)).first()

        if bill:
            cr_bill()
    elif case_type == 4:

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno) &  (Bill.flag == actflag) &  (Bill.zinr == roomno)).all():
            cr_bill()
    elif case_type == 5:

        bill = db_session.query(Bill).filter(
                (Bill._recid == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 6:

        bill = db_session.query(Bill).filter(
                (Bill.flag == actflag) &  (Bill.datum >= datum1) &  (Bill.datum <= datum2) &  (Bill.saldo != 0)).first()

        if bill:
            cr_bill()
    elif case_type == 7:

        bill = db_session.query(Bill).filter(
                (Bill.flag == actflag) &  ((Bill.saldo >= saldo1) |  (Bill.saldo <= - saldo2))).first()

        if bill:
            cr_bill()
    elif case_type == 8:

        bill = db_session.query(Bill).filter(
                (Bill.flag == actflag) &  (Bill.vesrdepot == roomno) &  (Billtyp == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 9:

        bill = db_session.query(Bill).filter(
                (Bill.flag == actflag) &  (Bill.rechnr == reslinno) &  (Bill.resnr == resno) &  (Bill.reslinnr == 1) &  (Billtyp == billno)).first()

        if bill:
            cr_bill()
    elif case_type == 10:

        bill_obj_list = []
        for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.reslinnr == Bill.reslinnr)).filter(
                (Bill.zinr == roomno) &  (Bill.flag == actflag)).all():
            if bill._recid in bill_obj_list:
                continue
            else:
                bill_obj_list.append(bill._recid)


            cr_bill()
    elif case_type == 11:

        for bill in db_session.query(Bill).filter(
                (Bill.zinr == roomno) &  (Bill.flag == actflag)).all():
            cr_bill()
    elif case_type == 12:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resno) &  (Bill.parent_nr == reslinno) &  (Bill.parent_nr != 0) &  (Billnr == billno) &  (Bill.flag == actflag) &  (Bill.zinr == roomno)).first()

        if bill:
            cr_bill()

    return generate_output()