#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 8/9/2025
# isi kolom tidak sama
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest, Bill, Bill_line, Bediener, Queasy, Reservation, History

def bil_selectbl(pvilanguage:int, sorttype:int, zinr:string, bil_int:int, curr_gastnr:int, ci_date:date, gastname:string, to_name:string, rechnr:int):

    prepare_cache ([Res_line, Guest, Bill, Bediener, Queasy, Reservation, History])

    b1_list_data = []
    actflag:int = 0
    bl_saldo:Decimal = to_decimal("0.0")
    lvcarea:string = "bil-select"
    res_line = guest = bill = bill_line = bediener = queasy = reservation = history = None

    b1_list = resline = rline = guestmember = mbill = bbuff = tbuff = None

    b1_list_data, B1_list = create_model("B1_list", {"zinr":string, "billnr":int, "rechnr":int, "name":string, "saldo":Decimal, "resnr":int, "reslinnr":int, "datum":date, "printnr":int, "vesrcod":string, "rec_id":int, "fg_col":bool, "resname":string, "address":string, "city":string, "b_comments":string, "guest_name":string, "repeat_charge":bool})

    Resline = create_buffer("Resline",Res_line)
    Rline = create_buffer("Rline",Res_line)
    Guestmember = create_buffer("Guestmember",Guest)
    Mbill = create_buffer("Mbill",Bill)
    Bbuff = create_buffer("Bbuff",Bill)
    Tbuff = create_buffer("Tbuff",Bill)


    db_session = local_storage.db_session

    #Rd 8/9/2025
    gastname = gastname.strip()
    to_name = to_name.strip()
    zinr = zinr.strip()

    def generate_output():
        nonlocal b1_list_data, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, queasy, reservation, history
        nonlocal pvilanguage, sorttype, zinr, bil_int, curr_gastnr, ci_date, gastname, to_name, rechnr
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff
        nonlocal b1_list_data

        return {"b1-list": b1_list_data}

    def disp_bill_list0():

        nonlocal b1_list_data, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, queasy, reservation, history
        nonlocal pvilanguage, sorttype, zinr, bil_int, curr_gastnr, ci_date, gastname, rechnr
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff
        nonlocal b1_list_data

        to_rechnr:int = 0
        fr_name:string = ""
        to_name:string = ""
        rmno:string = ""

        if sorttype == 1:

            if bil_int == 0:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag == 1) & (Res_line.zinr == (zinr).lower()) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
                        bl_saldo =  to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                            bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

                        if bill.zinr != res_line.zinr:
                            bbuff = db_session.query(Bbuff).filter(Bbuff._recid == bill._recid).with_for_update().first()
                            bbuff.zinr = res_line.zinr

                        if bl_saldo != bill.saldo:
                            tbuff = db_session.query(Tbuff).filter(Tbuff._recid == bill._recid).with_for_update().first()
                            tbuff.saldo =  to_decimal(bl_saldo)


            if trim(zinr) == "":

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr >= (zinr).lower()) & (Bill.zinr != "") & (Bill.flag == bil_int)).order_by(Bill.zinr, Bill.billnr).all():

                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

            else:

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((get_index(Bill.zinr, trim(zinr)) > 0) & (Bill.zinr != "") & (Bill.flag == bil_int)).order_by(Bill.zinr, Bill.billnr).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

        elif sorttype == 2:

            if curr_gastnr == 0:

                if gastname == "":
                    gastname = "a"

                if gastname.lower()  == ("*").lower() :
                    to_name = "zz"
                else:
                    fr_name = gastname
                    to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.name >= (fr_name).lower()) & (Bill.name <= (to_name).lower()) & (Bill.billtyp == 0)).order_by(Bill.name, Bill.zinr).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

                b1_list = query(b1_list_data, first=True)

                if not b1_list:

                    bill_obj_list = {}
                    bill = Bill()
                    rline = Res_line()
                    for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.name >= (fr_name).lower()) & (Bill.billtyp == 0)).order_by(Bill.name, Bill.zinr).all():
                        # if bill_obj_list.get(bill._recid):
                        #     continue
                        # else:
                        #     bill_obj_list[bill._recid] = True


                        assign_it()

            else:

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.gastnr == curr_gastnr) & (Bill.billtyp == 0)).order_by(Bill.name, Bill.zinr.desc()).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

        elif sorttype == 3:
            to_rechnr = rechnr + 1000

            bill_obj_list = {}
            bill = Bill()
            rline = Res_line()
            for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.rechnr == rechnr)).order_by(Bill.rechnr).all():
                # if bill_obj_list.get(bill._recid):
                #     continue
                # else:
                #     bill_obj_list[bill._recid] = True


                assign_it()

            b1_list = query(b1_list_data, first=True)

            if not b1_list:

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.rechnr >= rechnr) & (Bill.rechnr <= to_rechnr)).order_by(Bill.rechnr).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

        elif sorttype == 4:

            for rline in db_session.query(Rline).filter(
                     (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.abreise == ci_date) & (Rline.l_zuordnung[inc_value(2)] == 0)).order_by(Rline.zinr).all():

                for bill in db_session.query(Bill).filter(
                         (Bill.resnr == rline.resnr) & (Bill.parent_nr == rline.reslinnr) & (Bill.flag == 0)).order_by(Bill.billnr).all():
                    assign_it()


    def disp_bill_list1():

        nonlocal b1_list_data, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, queasy, reservation, history
        nonlocal pvilanguage, sorttype, zinr, bil_int, curr_gastnr, ci_date, gastname, rechnr
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff
        nonlocal b1_list_data

        to_rechnr:int = 0
        fr_name:string = ""
        to_name:string = ""
        rmno:string = ""

        if sorttype == 1:

            if zinr != "":

                if bil_int == 0:

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag == 1) & (Res_line.zinr == (zinr).lower()) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                        for bill in db_session.query(Bill).filter(
                                 (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
                            bl_saldo =  to_decimal("0")

                            for bill_line in db_session.query(Bill_line).filter(
                                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                                bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

                            if bill.zinr != res_line.zinr:
                                bbuff = db_session.query(Bbuff).filter(Bbuff._recid == bill._recid).with_for_update().first()
                                bbuff.zinr = res_line.zinr

                            if bl_saldo != bill.saldo:
                                bbuff = db_session.query(Bbuff).filter(Bbuff._recid == bill._recid).with_for_update().first()
                                bbuff.saldo =  to_decimal(bl_saldo)


                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr == (zinr).lower()) & (Bill.flag == bil_int) & (Bill.rechnr != 0)).order_by(Bill.rechnr.desc()).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

        elif sorttype == 2:

            if curr_gastnr == 0:

                if gastname == "":
                    gastname = "a"

                if gastname.lower()  == ("*").lower() :
                    to_name = "zz"
                else:
                    fr_name = gastname
                    to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.name >= (gastname).lower()) & (Bill.name <= (to_name).lower()) & (Bill.billtyp == 0) & (Bill.rechnr != 0)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

                b1_list = query(b1_list_data, first=True)

                if not b1_list:

                    bill_obj_list = {}
                    bill = Bill()
                    rline = Res_line()
                    for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.name >= (gastname).lower()) & (Bill.billtyp == 0) & (Bill.rechnr != 0)).order_by(Bill.name, Bill.rechnr.desc()).all():
                        # if bill_obj_list.get(bill._recid):
                        #     continue
                        # else:
                        #     bill_obj_list[bill._recid] = True


                        assign_it()

            else:

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.abreise == ci_date)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.gastnr == curr_gastnr) & (Bill.billtyp == 0) & (Bill.rechnr != 0)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

        elif sorttype == 3:

            if rechnr != 0:

                bill_obj_list = {}
                bill = Bill()
                rline = Res_line()
                for bill.zinr, bill.flag, bill.name, bill.datum, bill.parent_nr, bill.printnr, bill.rechnr, bill.saldo, bill.billnr, bill.reslinnr, bill.vesrcod, bill.parent_nr, bill._recid, rline.resnr, rline.reslinnr, rline.zinr, rline._recid, rline.gastnrmember, rline.abreise, rline.bemerk in db_session.query(Bill.zinr, Bill.flag, Bill.name, Bill.datum, Bill.parent_nr, Bill.printnr, Bill.rechnr, Bill.saldo, Bill.billnr, Bill.reslinnr, Bill.vesrcod, Bill.parent_nr, Bill._recid, Rline.resnr, Rline.reslinnr, Rline.zinr, Rline._recid, Rline.gastnrmember, Rline.abreise, Rline.bemerk).join(Rline,(Rline.resnr == Bill.resnr) & (Rline.reslinnr == Bill.parent_nr) & (Rline.active_flag == actflag)).filter((Bill.zinr > "") & (Bill.flag == bil_int) & (Bill.rechnr == rechnr)).order_by(Bill._recid).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True

                    assign_it()

        elif sorttype == 4:

            for rline in db_session.query(Rline).filter(
                     (Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.abreise == ci_date) & (Rline.l_zuordnung[inc_value(2)] == 0)).order_by(Rline.zinr).all():

                for bill in db_session.query(Bill).filter(
                         (Bill.resnr == rline.resnr) & (Bill.parent_nr == rline.reslinnr) & (Bill.flag == 1)).order_by(Bill.billnr).all():
                    
                    assign_it()


    def assign_it():

        nonlocal b1_list_data, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, queasy, reservation, history
        nonlocal pvilanguage, sorttype, zinr, bil_int, curr_gastnr, ci_date, gastname, to_name, rechnr
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff
        nonlocal b1_list_data

        usr = None
        Usr =  create_buffer("Usr",Bediener)
        bl_saldo =  to_decimal("0")

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)]})
        while None != bill_line:
            bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

            curr_recid = bill_line._recid
            bill_line = db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line._recid > curr_recid)).first()

        if bl_saldo != bill.saldo:
            tbuff = db_session.query(Tbuff).filter(Tbuff._recid == bill._recid).with_for_update().first()
            tbuff.saldo =  to_decimal(bl_saldo)

        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.zinr = bill.zinr
        b1_list.billnr = bill.billnr
        b1_list.rechnr = bill.rechnr
        b1_list.name = bill.name
        b1_list.saldo =  to_decimal(bill.saldo)
        b1_list.resnr = bill.resnr
        b1_list.reslinnr = bill.reslinnr
        b1_list.datum = bill.datum
        b1_list.printnr = bill.printnr
        b1_list.vesrcod = bill.vesrcod
        b1_list.rec_id = bill._recid

        mbill = get_cache (Bill, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, 0)]})

        if mbill:
            b1_list.fg_col = True

        queasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, bill.resnr)],"logi1": [(eq, True)]})

        if queasy:
            b1_list.repeat_charge = queasy.logi1

        usr = get_cache (Bediener, {"userinit": [(eq, bill.vesrcod)]})

        if usr:
            b1_list.b_comments = translateExtended ("C/O by:", lvcarea, "") + " " + usr.username + chr_unicode(10)

        if bill:

            reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})

            if reservation:

                resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                if resline:

                    guestmember = get_cache (Guest, {"gastnr": [(eq, resline.gastnrmember)]})
                    b1_list.resname = guestmember.name + ", " + guestmember.vorname1 + " " + guestmember.anrede1
                    b1_list.guest_name = guestmember.anrede1 + " " + guestmember.name + ", " + guestmember.vorname1
                    b1_list.address = guestmember.adresse1
                    b1_list.city = guestmember.wohnort + " " + guestmember.plz
                    b1_list.b_comments = b1_list.b_comments + translateExtended ("Departure:", lvcarea, "") + " " + to_string(resline.abreise) + chr_unicode(10)

                    if guestmember.bemerkung != "":
                        b1_list.b_comments = b1_list.b_comments + guestmember.bemerkung + chr_unicode(10)

                    if reservation.bemerk != "":
                        b1_list.b_comments = b1_list.b_comments + reservation.bemerk + chr_unicode(10)

                    if resline.bemerk != "":
                        b1_list.b_comments = b1_list.b_comments + resline.bemerk
            else:

                if bill.flag == 1:

                    history = get_cache (History, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)],"zi_wechsel": [(eq, False)]})

                    if history:

                        guestmember = get_cache (Guest, {"gastnr": [(eq, history.gastnr)]})
                        b1_list.resname = guestmember.name + ", " + guestmember.vorname1 + " " + guestmember.anrede1
                        b1_list.guest_name = guestmember.anrede1 + " " + guestmember.name + ", " + guestmember.vorname1
                        b1_list.address = guestmember.adresse1
                        b1_list.city = guestmember.wohnort + " " + guestmember.plz
                        b1_list.b_comments = b1_list.b_comments + translateExtended ("Departure:", lvcarea, "") + " " + to_string(history.abreise) + chr_unicode(10)
                        b1_list.b_comments = b1_list.b_comments + history.bemerk

    actflag = bil_int + 1

    if bil_int == 0:
        disp_bill_list0()
    else:
        disp_bill_list1()

    return generate_output()