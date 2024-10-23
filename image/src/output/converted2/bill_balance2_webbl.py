from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Htparam, Bill, Bill_line, Hoteldpt, Res_line, Queasy, History, Reservation

def bill_balance2_webbl(pvilanguage:int, co_today:bool, room:str, zero_flag:bool, cash_basis:bool, gname:str, billdate:date, menu_nsbill:bool, menu_msbill:bool, menu_fobill:bool):
    billbalance_list_list = []
    tot_outstand:decimal = to_decimal("0.0")
    bill_saldo:decimal = to_decimal("0.0")
    tot_saldo:decimal = to_decimal("0.0")
    do_it:bool = False
    ci_date:date = None
    lvcarea:str = "bill-balance"
    guest = htparam = bill = bill_line = hoteldpt = res_line = queasy = history = reservation = None

    billbalance_list = gast = None

    billbalance_list_list, Billbalance_list = create_model("Billbalance_list", {"flag":str, "departnem":str, "zinr":str, "resstatus":int, "zipreis":decimal, "rechnr":int, "receiver":str, "ankunft":date, "abreise":date, "saldo":decimal, "name":str, "bill_inst":str, "idcard":str, "nat":str, "datum":date, "fsort":str, "remarks":str, "bill_remark":str}, {"ankunft": None, "abreise": None})

    Gast = create_buffer("Gast",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billbalance_list_list, tot_outstand, bill_saldo, tot_saldo, do_it, ci_date, lvcarea, guest, htparam, bill, bill_line, hoteldpt, res_line, queasy, history, reservation
        nonlocal pvilanguage, co_today, room, zero_flag, cash_basis, gname, billdate, menu_nsbill, menu_msbill, menu_fobill
        nonlocal gast


        nonlocal billbalance_list, gast
        nonlocal billbalance_list_list
        return {"billbalance-list": billbalance_list_list}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if not cash_basis:

        if not co_today:

            if room == "":

                if menu_nsbill:

                    for bill in db_session.query(Bill).filter(
                             (Bill.flag == 0) & (Bill.resnr == 0)).order_by(Bill.name).all():
                        do_it = False
                        bill_saldo =  to_decimal("0")

                        if (zero_flag and bill.datum != None and bill.name != "") or bill.saldo != 0:
                            do_it = True

                        if do_it:
                            billbalance_list = Billbalance_list()
                            billbalance_list_list.append(billbalance_list)


                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == bill.gastnr)).first()

                            if guest:

                                for bill_line in db_session.query(Bill_line).filter(
                                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line._recid).all():
                                    bill_saldo =  to_decimal(bill_saldo) + to_decimal(bill_line.betrag)
                                tot_saldo =  to_decimal(tot_saldo) + to_decimal(bill_saldo)
                                billbalance_list.flag = "NS"
                                billbalance_list.receiver = bill.name
                                billbalance_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                        guest.anrede1 + guest.anredefirma
                                billbalance_list.rechnr = bill.rechnr
                                billbalance_list.saldo =  to_decimal(bill_saldo)
                                billbalance_list.ankunft = None
                                billbalance_list.abreise = None
                                billbalance_list.idcard = guest.ausweis_nr1
                                billbalance_list.nat = guest.nation1
                                billbalance_list.datum = bill.datum
                                billbalance_list.fsort = "0"
                                billbalance_list.bill_remark = bill.vesrdepot

                                hoteldpt = db_session.query(Hoteldpt).filter(
                                         (Hoteldpt.num == bill.billtyp)).first()

                                if hoteldpt:
                                    billbalance_list.departnem = hoteldpt.depart
                                billbalance_list.remarks = guest.bemerkung
                            tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)

            if room == "" and menu_msbill:

                for bill in db_session.query(Bill).filter(
                         (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.reslinnr == 0)).order_by(Bill.name).all():
                    do_it = False
                    bill_saldo =  to_decimal("0")

                    if zero_flag or bill.saldo != 0:
                        do_it = True

                    if do_it:
                        billbalance_list = Billbalance_list()
                        billbalance_list_list.append(billbalance_list)


                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill.resnr) & (Res_line.resstatus <= 8)).first()

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnrmember)).first()

                        if guest:

                            for bill_line in db_session.query(Bill_line).filter(
                                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line._recid).all():
                                bill_saldo =  to_decimal(bill_saldo) + to_decimal(bill_line.betrag)
                            tot_saldo =  to_decimal(tot_saldo) + to_decimal(bill_saldo)
                            billbalance_list.flag = "M"
                            billbalance_list.receiver = bill.name
                            billbalance_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                    guest.anrede1 + guest.anredefirma
                            billbalance_list.name = ""
                            billbalance_list.rechnr = bill.rechnr
                            billbalance_list.saldo =  to_decimal(bill_saldo)
                            billbalance_list.idcard = guest.ausweis_nr1
                            billbalance_list.nat = guest.nation1
                            billbalance_list.datum = bill.datum
                            billbalance_list.fsort = "0"
                            billbalance_list.bill_remark = bill.vesrdepot

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                 (Hoteldpt.num == 0)).first()

                        if hoteldpt:
                            billbalance_list.departnem = hoteldpt.depart

                        if res_line:
                            billbalance_list.ankunft = res_line.ankunft
                            billbalance_list.abreise = res_line.abreise
                            billbalance_list.resstatus = res_line.resstatus
                            billbalance_list.remarks = guest.bemerkung + res_line.bemerk + bill.vesrdepot

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

                            if queasy:
                                billbalance_list.bill_inst = queasy.char1
                        else:

                            history = db_session.query(History).filter(
                                     (History.resnr == bill.resnr) & (History.reslinnr < 999) & (History.zi_wechsel == False)).first()

                            if history:
                                billbalance_list.ankunft = history.ankunft
                                billbalance_list.abreise = history.abreise


                        tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)

        if co_today:

            if menu_fobill:

                bill_obj_list = []
                for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr) & (Res_line.abreise == ci_date)).filter(
                         (Bill.flag == 0) & (Bill.resnr > 0) & (func.lower(Bill.zinr) != "") & (func.lower(Bill.zinr) >= (room).lower())).order_by(Bill.zinr, Bill.reslinnr).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    do_it = False
                    bill_saldo =  to_decimal("0")

                    if zero_flag or bill.saldo != 0:
                        do_it = True

                    if gname != "":

                        reservation = db_session.query(Reservation).filter(
                                 (func.lower(Reservation.groupname) == (gname).lower()) & (Reservation.resnr == bill.resnr)).first()

                        if not reservation:
                            do_it = False

                    if do_it:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnrmember)).first()
                        billbalance_list = Billbalance_list()
                        billbalance_list_list.append(billbalance_list)

                        billbalance_list.zinr = bill.zinr
                        billbalance_list.resstatus = res_line.resstatus

                        if res_line.resstatus != 12:
                            billbalance_list.name = res_line.name
                        else:
                            billbalance_list.name = translateExtended ("** Extra Bill", lvcarea, "")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line._recid).all():
                            bill_saldo =  to_decimal(bill_saldo) + to_decimal(bill_line.betrag)
                        tot_saldo =  to_decimal(tot_saldo) + to_decimal(bill_saldo)
                        billbalance_list.receiver = bill.name
                        billbalance_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        billbalance_list.zipreis =  to_decimal(res_line.zipreis)
                        billbalance_list.rechnr = bill.rechnr
                        billbalance_list.saldo =  to_decimal(bill_saldo)
                        billbalance_list.ankunft = res_line.ankunft
                        billbalance_list.abreise = res_line.abreise
                        billbalance_list.idcard = guest.ausweis_nr1
                        billbalance_list.nat = guest.nation1
                        billbalance_list.datum = bill.datum
                        billbalance_list.fsort = "0"
                        billbalance_list.remarks = guest.bemerkung + res_line.bemerk + bill.vesrdepot
                        billbalance_list.bill_remark = bill.vesrdepot

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                 (Hoteldpt.num == 0)).first()

                        if hoteldpt:
                            billbalance_list.departnem = hoteldpt.depart

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy:
                            billbalance_list.bill_inst = queasy.char1
                        tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)

        elif menu_fobill:

            for bill in db_session.query(Bill).filter(
                     (Bill.flag == 0) & (Bill.resnr > 0) & (func.lower(Bill.zinr) != "") & (func.lower(Bill.zinr) >= (room).lower())).order_by(Bill.zinr, Bill.reslinnr).all():

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.reslinnr)).first()

                if not res_line:

                    history = db_session.query(History).filter(
                             (History.resnr == bill.resnr) & (History.reslinnr == bill.reslinnr) & (not History.zi_wechsel)).first()
                do_it = False
                bill_saldo =  to_decimal("0")

                if zero_flag or bill.saldo != 0:
                    do_it = True

                if gname != "":

                    reservation = db_session.query(Reservation).filter(
                             (func.lower(Reservation.groupname) == (gname).lower()) & (Reservation.resnr == bill.resnr)).first()

                    if not reservation:
                        do_it = False

                if do_it:

                    if res_line:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnrmember)).first()
                    else:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == bill.gastnr)).first()
                    billbalance_list = Billbalance_list()
                    billbalance_list_list.append(billbalance_list)


                    if res_line and res_line.resstatus != 12:
                        billbalance_list.name = res_line.name
                    else:
                        billbalance_list.name = translateExtended ("** Extra Bill", lvcarea, "")

                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line._recid).all():
                        bill_saldo =  to_decimal(bill_saldo) + to_decimal(bill_line.betrag)
                    tot_saldo =  to_decimal(tot_saldo) + to_decimal(bill_saldo)
                    billbalance_list.zinr = bill.zinr
                    billbalance_list.receiver = bill.name
                    billbalance_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    billbalance_list.rechnr = bill.rechnr
                    billbalance_list.saldo =  to_decimal(bill_saldo)
                    billbalance_list.idcard = guest.ausweis_nr1
                    billbalance_list.nat = guest.nation1
                    billbalance_list.datum = bill.datum
                    billbalance_list.fsort = "0"
                    billbalance_list.bill_remark = bill.vesrdepot

                    hoteldpt = db_session.query(Hoteldpt).filter(
                             (Hoteldpt.num == 0)).first()

                    if hoteldpt:
                        billbalance_list.departnem = hoteldpt.depart

                    if res_line:
                        billbalance_list.ankunft = res_line.ankunft
                        billbalance_list.abreise = res_line.abreise
                        billbalance_list.zipreis =  to_decimal(res_line.zipreis)
                        billbalance_list.resstatus = res_line.resstatus
                        billbalance_list.remarks = res_line.bemerk + bill.vesrdepot

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy:
                            billbalance_list.bill_inst = queasy.char1

                    elif history:
                        billbalance_list.ankunft = history.ankunft
                        billbalance_list.abreise = history.abreise
                        billbalance_list.zipreis =  to_decimal(history.zipreis)


                    tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)
    else:

        if co_today:

            if menu_fobill:

                bill_obj_list = []
                for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr) & (Res_line.abreise == ci_date)).filter(
                         (Bill.flag == 0) & (Bill.resnr > 0) & (func.lower(Bill.zinr) != "") & (func.lower(Bill.zinr) >= (room).lower())).order_by(Bill.zinr, Bill.reslinnr).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:
                        do_it = False
                        bill_saldo =  to_decimal("0")

                        if zero_flag or bill.saldo != 0:
                            do_it = True

                        if gname != "":

                            reservation = db_session.query(Reservation).filter(
                                     (func.lower(Reservation.groupname) == (gname).lower()) & (Reservation.resnr == bill.resnr)).first()

                            if not reservation:
                                do_it = False

                        if do_it:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()
                            billbalance_list = Billbalance_list()
                            billbalance_list_list.append(billbalance_list)

                            billbalance_list.zinr = bill.zinr
                            billbalance_list.resstatus = res_line.resstatus

                            if res_line.resstatus != 12:
                                billbalance_list.name = res_line.name
                            else:
                                billbalance_list.name = translateExtended ("** Extra Bill", lvcarea, "")

                            for bill_line in db_session.query(Bill_line).filter(
                                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line._recid).all():
                                bill_saldo =  to_decimal(bill_saldo) + to_decimal(bill_line.betrag)
                            tot_saldo =  to_decimal(tot_saldo) + to_decimal(bill_saldo)
                            billbalance_list.name = res_line.name
                            billbalance_list.receiver = bill.name
                            billbalance_list.zipreis =  to_decimal(res_line.zipreis)
                            billbalance_list.rechnr = bill.rechnr
                            billbalance_list.saldo =  to_decimal(bill_saldo)
                            billbalance_list.ankunft = res_line.ankunft
                            billbalance_list.abreise = res_line.abreise
                            billbalance_list.idcard = guest.ausweis_nr1
                            billbalance_list.nat = guest.nation1
                            billbalance_list.datum = bill.datum
                            billbalance_list.fsort = "0"
                            billbalance_list.remarks = res_line.bemerk + bill.vesrdepot
                            billbalance_list.bill_remark = bill.vesrdepot

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                     (Hoteldpt.num == 0)).first()

                            if hoteldpt:
                                billbalance_list.departnem = hoteldpt.depart

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

                            if queasy:
                                billbalance_list.bill_inst = queasy.char1
                            tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)
        else:

            if menu_fobill:

                for bill in db_session.query(Bill).filter(
                         (Bill.flag == 0) & (Bill.resnr > 0) & (func.lower(Bill.zinr) != "") & (func.lower(Bill.zinr) >= (room).lower())).order_by(Bill.zinr, Bill.reslinnr).all():
                    do_it = False
                    bill_saldo =  to_decimal("0")

                    if zero_flag or bill.saldo != 0:
                        do_it = True

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:

                        if do_it:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == bill.gastnr)).first()

                            for bill_line in db_session.query(Bill_line).filter(
                                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line._recid).all():
                                bill_saldo =  to_decimal(bill_saldo) + to_decimal(bill_line.betrag)
                            tot_saldo =  to_decimal(tot_saldo) + to_decimal(bill_saldo)
                            billbalance_list = Billbalance_list()
                            billbalance_list_list.append(billbalance_list)

                            billbalance_list.resstatus = res_line.resstatus
                            billbalance_list.zinr = bill.zinr
                            billbalance_list.name = res_line.name
                            billbalance_list.receiver = bill.name
                            billbalance_list.rechnr = bill.rechnr
                            billbalance_list.saldo =  to_decimal(bill_saldo)
                            billbalance_list.idcard = guest.ausweis_nr1
                            billbalance_list.nat = guest.nation1
                            billbalance_list.datum = bill.datum
                            billbalance_list.fsort = "0"
                            billbalance_list.ankunft = res_line.ankunft
                            billbalance_list.abreise = res_line.abreise
                            billbalance_list.zipreis =  to_decimal(res_line.zipreis)
                            billbalance_list.bill_inst = queasy.char1
                            billbalance_list.remarks = guest.bemerkung + res_line.bemerk + bill.vesrdepot
                            billbalance_list.bill_remark = bill.vesrdepot

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                     (Hoteldpt.num == 0)).first()

                            if hoteldpt:
                                billbalance_list.departnem = hoteldpt.depart
                            tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)
    tot_outstand =  to_decimal("0")

    for billbalance_list in query(billbalance_list_list):
        tot_outstand =  to_decimal(tot_outstand) + to_decimal(billbalance_list.saldo)
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr(10) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr(13) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "~n", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "\\n", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "~r", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "~r~n", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "&nbsp;", " ")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "</p>", chr(13))
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "<BR>", chr(13))
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr(10) + chr(13) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr(2) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr(3) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr(4) , "")

        if len(billbalance_list.remarks) < 3:
            billbalance_list.remarks = replace_str(billbalance_list.remarks, chr(32) , "")

        if len(billbalance_list.remarks) < 3:
            billbalance_list.remarks = ""

        if len(billbalance_list.remarks) == None:
            billbalance_list.remarks = ""
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr(10) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr(13) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "~n", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "\\n", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "~r", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "~r~n", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "&nbsp;", " ")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "</p>", chr(13))
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "<BR>", chr(13))
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr(10) + chr(13) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr(2) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr(3) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr(4) , "")

        if len(billbalance_list.bill_remark) < 3:
            billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr(32) , "")

        if len(billbalance_list.bill_remark) < 3:
            billbalance_list.bill_remark = ""

        if len(billbalance_list.bill_remark) == None:
            billbalance_list.bill_remark = ""
    billbalance_list = Billbalance_list()
    billbalance_list_list.append(billbalance_list)

    billbalance_list.receiver = "T o t a l"
    billbalance_list.saldo =  to_decimal(tot_outstand)
    billbalance_list.fsort = "1"

    return generate_output()