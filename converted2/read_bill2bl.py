#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import Bill, Res_line, Bill_line, Nebenst, Bk_veran, Bk_reser

def read_bill2bl(case_type:int, billno:int, resno:int, reslinno:int, actflag:int, roomno:string, datum1:date, datum2:date, saldo1:Decimal, saldo2:Decimal):

    prepare_cache ([Bill, Bill_line, Bk_veran])

    telbill_flag = False
    babill_flag = False
    t_bill_data = []
    ba_dept:int = 0
    bill_date:date = None
    bl_saldo:Decimal = to_decimal("0.0")
    bill = res_line = bill_line = nebenst = bk_veran = bk_reser = None

    t_bill = tbuff = None

    t_bill_data, T_bill = create_model("T_bill", {"zinr":string, "flag":int, "rechnr":int, "resnr":int, "gastnr":int, "saldo":Decimal, "gesamtumsatz":Decimal, "logisumsatz":Decimal, "arrangemdat":date, "rgdruck":int, "logiernachte":int, "reslinnr":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "billnr":int, "firstper":bool, "billkur":bool, "logidat":date, "bilname":string, "teleinheit":int, "telsumme":Decimal, "segmentcode":int, "printnr":int, "billbankett":bool, "service":[Decimal,99], "mwst":[Decimal,99], "umleit_zinr":string, "billmaster":bool, "datum":date, "taxsumme":Decimal, "name":string, "billtyp":int, "parent_nr":int, "restargt":Decimal, "init_argt":Decimal, "rest_tage":int, "ums_kurz":Decimal, "ums_lang":Decimal, "nextargt_bookdate":date, "roomcharge":bool, "oldzinr":string, "t_rechnr":int, "rechnr2":int, "betriebsnr":int, "vesrdep":Decimal, "vesrdat":date, "vesrdepot":string, "vesrdepot2":string, "vesrcod":string, "verstat":int, "kontakt_nr":int, "betrieb_gast":int, "billref":int, "bl_recid":int})

    Tbuff = create_buffer("Tbuff",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal telbill_flag, babill_flag, t_bill_data, ba_dept, bill_date, bl_saldo, bill, res_line, bill_line, nebenst, bk_veran, bk_reser
        nonlocal case_type, billno, resno, reslinno, actflag, roomno, datum1, datum2, saldo1, saldo2
        nonlocal tbuff


        nonlocal t_bill, tbuff
        nonlocal t_bill_data

        return {"telbill_flag": telbill_flag, "babill_flag": babill_flag, "t-bill": t_bill_data}

    def cr_bill():

        nonlocal telbill_flag, babill_flag, t_bill_data, ba_dept, bill_date, bl_saldo, bill, res_line, bill_line, nebenst, bk_veran, bk_reser
        nonlocal case_type, billno, resno, reslinno, actflag, roomno, datum1, datum2, saldo1, saldo2
        nonlocal tbuff


        nonlocal t_bill, tbuff
        nonlocal t_bill_data


        bl_saldo =  to_decimal("0")

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
            bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

        if bl_saldo != bill.saldo:

            tbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
            tbuff.saldo =  to_decimal(bl_saldo)
            pass
            pass
        t_bill = T_bill()
        t_bill_data.append(t_bill)

        buffer_copy(bill, t_bill,except_fields=["bill.vesrdepot"])
        t_bill.vesrdepot = bill.vesrdepot
        t_bill.bl_recid = bill._recid

        if bill.rechnr > 0:

            nebenst = get_cache (Nebenst, {"zinr": [(eq, "")],"rechnr": [(eq, bill.rechnr)]})
            telbill_flag = None != nebenst

            if ba_dept > 0 and bill.billtyp == ba_dept:
                check_banquet()


    def check_banquet():

        nonlocal telbill_flag, babill_flag, t_bill_data, ba_dept, bill_date, bl_saldo, bill, res_line, bill_line, nebenst, bk_veran, bk_reser
        nonlocal case_type, billno, resno, reslinno, actflag, roomno, datum1, datum2, saldo1, saldo2
        nonlocal tbuff


        nonlocal t_bill, tbuff
        nonlocal t_bill_data

        bk_veran = get_cache (Bk_veran, {"rechnr": [(eq, bill.rechnr)]})

        if bk_veran and bk_veran.activeflag == 0:

            bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"datum": [(gt, bill_date)],"resstatus": [(le, 3)]})

            if bk_reser:
                babill_flag = True

                return

            bk_reser = db_session.query(Bk_reser).filter(
                     (Bk_reser.veran_nr == bk_veran.veran_nr) & (Bk_reser.datum == bill_date) & (Bk_reser.resstatus == 1) & ((Bk_reser.bis_i * 1800) > get_current_time_in_seconds())).first()

            if bk_reser:
                babill_flag = True

                return

    bill_date = get_output(htpdate(110))
    ba_dept = get_output(htpint(900))

    if ba_dept == 0:
        ba_dept = -1

    if case_type == 1:

        bill = get_cache (Bill, {"rechnr": [(eq, billno)]})

        if bill:
            cr_bill()
    elif case_type == 2:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.parent_nr != 0) & (Bill.flag == actflag) & (Bill.zinr == roomno)).order_by(Bill._recid).all():
            cr_bill()
    elif case_type == 3:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"parent_nr": [(eq, reslinno)],"billnr": [(eq, billno)],"flag": [(eq, actflag)],"zinr": [(eq, roomno)]})

        if bill:
            cr_bill()
    elif case_type == 4:

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == resno) & (Bill.parent_nr == reslinno) & (Bill.flag == actflag) & (Bill.zinr == roomno)).order_by(Bill._recid).all():
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
    elif case_type == 10:

        bill_obj_list = {}
        for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr)).filter(
                 (Bill.zinr == roomno) & (Bill.flag == actflag)).order_by(Bill._recid).all():
            if bill_obj_list.get(bill._recid):
                continue
            else:
                bill_obj_list[bill._recid] = True


            cr_bill()
    elif case_type == 11:

        for bill in db_session.query(Bill).filter(
                 (Bill.zinr == roomno) & (Bill.flag == actflag)).order_by(Bill._recid).all():
            cr_bill()
    elif case_type == 12:

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"parent_nr": [(eq, reslinno),(ne, 0)],"billnr": [(eq, billno)],"flag": [(eq, actflag)],"zinr": [(eq, roomno)]})

        if bill:
            cr_bill()
    elif case_type == 13:

        bill = get_cache (Bill, {"gastnr": [(eq, resno)],"flag": [(eq, actflag)],"vesrdepot2": [(eq, roomno)]})

        if bill:
            cr_bill()

    return generate_output()