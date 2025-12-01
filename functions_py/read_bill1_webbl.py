#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 05/11/2025
# Rd, 27/11/2025, with_for_update
#-------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Res_line, Queasy, Bill_line

def read_bill1_webbl(case_type:int, billno:int, resno:int, reslinno:int, actflag:int, roomno:string, datum1:date, datum2:date, saldo1:Decimal, saldo2:Decimal):

    prepare_cache ([Bill, Res_line, Queasy, Bill_line])

    t_bill_data = []
    bl_saldo:Decimal = to_decimal("0.0")
    bill = res_line = queasy = bill_line = None

    t_bill = rline = bbuff = bqueasy = tbuff = None

    t_bill_data, T_bill = create_model_like(Bill, {"bl_recid":int, "repeat_charge":bool})

    Rline = create_buffer("Rline",Res_line)
    Bbuff = create_buffer("Bbuff",Bill)
    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tbuff = create_buffer("Tbuff",Bill)


    db_session = local_storage.db_session
    roomno = roomno.strip()

    def generate_output():
        nonlocal t_bill_data, bl_saldo, bill, res_line, queasy, bill_line
        nonlocal case_type, billno, resno, reslinno, actflag, roomno, datum1, datum2, saldo1, saldo2
        nonlocal rline, bbuff, bqueasy, tbuff


        nonlocal t_bill, rline, bbuff, bqueasy, tbuff
        nonlocal t_bill_data

        return {"t-bill": t_bill_data}

    def cr_bill():

        nonlocal t_bill_data, bl_saldo, bill, res_line, queasy, bill_line
        nonlocal case_type, billno, resno, reslinno, actflag, roomno, datum1, datum2, saldo1, saldo2
        nonlocal rline, bbuff, bqueasy, tbuff


        nonlocal t_bill, rline, bbuff, bqueasy, tbuff
        nonlocal t_bill_data


        bl_saldo =  to_decimal("0")

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
            bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

        if bl_saldo != bill.saldo:

            # tbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
            tbuff = db_session.query(Bill).filter(Bill._recid == bill._recid).with_for_update().first()
            tbuff.saldo =  to_decimal(bl_saldo)
            pass
            pass
        t_bill = T_bill()
        t_bill_data.append(t_bill)

        pass
        buffer_copy(bill, t_bill)
        t_bill.bl_recid = bill._recid

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

        if res_line:

            bqueasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, res_line.resnr)],"logi1": [(eq, True)]})

            if bqueasy:
                repeat_charge = bqueasy.logi1


    if case_type == 1:

        bill = get_cache (Bill, {"rechnr": [(eq, billno)]})

        if bill:
            cr_bill()
    elif case_type == 2:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.parent_nr != 0) & (Bill.flag == actflag) & (Bill.zinr == roomno)).order_by(Bill.billnr).all():
            cr_bill()
    elif case_type == 3:

        # bill = get_cache (Bill, {"resnr": [(eq, resno)],"parent_nr": [(eq, reslinno)],"billnr": [(eq, billno)],"flag": [(eq, actflag)],"zinr": [(eq, roomno)]})
        bill = db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.billnr == billno) & (Bill.flag == actflag) & (Bill.zinr == roomno)).first()

        if bill:
            cr_bill()
    elif case_type == 4:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.flag == actflag) & (Bill.zinr == roomno)).order_by(Bill.billnr).all():
            cr_bill()
    elif case_type == 5:

        bill = get_cache (Bill, {"_recid": [(eq, billno)]})

        if bill:
            cr_bill()
    elif case_type == 6:

        bill = get_cache (Bill, {"flag": [(eq, actflag)],"datum": [(ge, datum1),(le, datum2)],"saldo": [(ne, 0)]})

        if bill:
            cr_bill()
    elif case_type == 7:

        bill = db_session.query(Bill).filter(
                 (Bill.flag == actflag) & ((Bill.saldo >= saldo1) | (Bill.saldo <= - saldo2))).first()

        if bill:
            cr_bill()
    elif case_type == 8:

        bill = get_cache (Bill, {"flag": [(eq, actflag)],"vesrdepot": [(eq, roomno)],"billtyp": [(eq, billno)]})

        if bill:
            cr_bill()
    elif case_type == 9:

        bill = get_cache (Bill, {"flag": [(eq, actflag)],"rechnr": [(eq, reslinno)],"resnr": [(eq, resno)],"reslinnr": [(eq, 1)],"billtyp": [(eq, billno)]})

        if bill:
            cr_bill()
    elif case_type == 10 or case_type == 11:

        if actflag == 0:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.zinr == roomno) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                for bill in db_session.query(Bill).filter(
                         (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():

                    if bill.zinr != res_line.zinr:

                        # bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                        bbuff = db_session.query(Bill).filter(Bill._recid == bill._recid).with_for_update().first()
                        bbuff.zinr = res_line.zinr


                        pass
                        pass
                    cr_bill()

        else:

            bill_obj_list = {}
            bill = Bill()
            res_line = Res_line()
            for bill.zinr, bill._recid, bill.saldo, res_line.resnr, res_line.reslinnr, res_line.zinr, res_line._recid in db_session.query(Bill.zinr, Bill._recid, Bill.saldo, Res_line.resnr, Res_line.reslinnr, Res_line.zinr, Res_line._recid).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr)).filter(
                     (Bill.zinr == roomno) & (Bill.flag == actflag)).order_by(Bill.billnr).all():
                if bill_obj_list.get(bill._recid):
                    continue
                else:
                    bill_obj_list[bill._recid] = True


                cr_bill()

    elif case_type == 12:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"parent_nr": [(eq, reslinno),(ne, 0)],"billnr": [(eq, billno)],"flag": [(eq, actflag)],"zinr": [(eq, roomno)]})

        if bill:
            cr_bill()

    return generate_output()