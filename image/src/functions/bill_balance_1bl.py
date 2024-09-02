from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Htparam, Bill, Hoteldpt, Reservation, Res_line, Bill_line, Queasy, History

def bill_balance_1bl(pvilanguage:int, co_today:bool, room:str, zero_flag:bool, cash_basis:bool, gname:str, menu_nsbill:bool, menu_msbill:bool, menu_fobill:bool):
    billbalance_list_list = []
    tot_outstand:decimal = 0
    do_it:bool = False
    ci_date:date = None
    lvcarea:str = "bill_balance"
    guest = htparam = bill = hoteldpt = reservation = res_line = bill_line = queasy = history = None

    billbalance_list = gast = None

    billbalance_list_list, Billbalance_list = create_model("Billbalance_list", {"flag":str, "departnem":str, "zinr":str, "resstatus":int, "zipreis":decimal, "rechnr":int, "receiver":str, "ankunft":date, "abreise":date, "saldo":decimal, "name":str, "bill_inst":str, "idcard":str, "nat":str, "datum":date, "fsort":str, "remarks":str, "bill_remark":str}, {"ankunft": None, "abreise": None})

    Gast = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billbalance_list_list, tot_outstand, do_it, ci_date, lvcarea, guest, htparam, bill, hoteldpt, reservation, res_line, bill_line, queasy, history
        nonlocal gast


        nonlocal billbalance_list, gast
        nonlocal billbalance_list_list
        return {"billbalance-list": billbalance_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = fdate

    if not cash_basis:

        if not co_today:

            if room == "":

                if menu_nsbill:

                    for bill in db_session.query(Bill).filter(
                            (Bill.flag == 0) &  (Bill.resnr == 0)).all():
                        do_it = False

                        if (zero_flag and bill.datum != None and bill.name != "") or bill.saldo != 0:
                            do_it = True

                        if do_it:
                            billbalance_list = Billbalance_list()
                            billbalance_list_list.append(billbalance_list)


                            guest = db_session.query(Guest).filter(
                                    (Guest.gastnr == bill.gastnr)).first()

                            if guest:
                                billbalance_list.flag = "NS"
                                billbalance_list.receiver = bill.name
                                billbalance_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                        guest.anrede1 + guest.anredefirma
                                billbalance_list.rechnr = bill.rechnr
                                billbalance_list.saldo = bill.saldo
                                billbalance_list.ankunft = None
                                billbalance_list.abreise = None
                                billbalance_list.idcard = guest.ausweis_nr1
                                billbalance_list.NAT = guest.nation1
                                billbalance_list.datum = bill.datum
                                billbalance_list.fsort = "0"
                                billbalance_list.bill_remark = bill.vesrdepot

                                hoteldpt = db_session.query(Hoteldpt).filter(
                                        (Hoteldpt.num == billtyp)).first()

                                if hoteldpt:
                                    billbalance_list.departnem = hoteldpt.depart

                                reservation = db_session.query(Reservation).filter(
                                        (Reservation.gastnr == bill.gastnr)).first()

                                if reservation:
                                    billbalance_list.remarks = guest.bemerk + reservation.bemerk + bill.vesrdepot
                                else:
                                    billbalance_list.remarks = guest.bemerk + bill.vesrdepot
                            tot_outstand = tot_outstand + bill.saldo


            if room == "" and menu_msbill:

                for bill in db_session.query(Bill).filter(
                        (Bill.flag == 0) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0)).all():
                    do_it = False

                    if zero_flag or bill.saldo != 0:
                        do_it = True

                    if do_it:
                        billbalance_list = Billbalance_list()
                        billbalance_list_list.append(billbalance_list)


                        res_line = db_session.query(Res_line).filter(
                                (Res_line.resnr == bill.resnr) &  (Res_line.resstatus <= 8)).first()

                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember)).first()

                        if guest:
                            billbalance_list.flag = "M"
                            billbalance_list.receiver = bill.name
                            billbalance_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                    guest.anrede1 + guest.anredefirma
                            billbalance_list.name = ""
                            billbalance_list.rechnr = bill.rechnr
                            billbalance_list.saldo = bill.saldo
                            billbalance_list.idcard = guest.ausweis_nr1
                            billbalance_list.NAT = guest.nation1
                            billbalance_list.datum = bill.datum
                            billbalance_list.fsort = "0"
                            billbalance_list.bill_remark = bill.vesrdepot

                        bill_line = db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == bill.rechnr)).first()

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                (Hoteldpt.num == 0)).first()

                        if hoteldpt:
                            billbalance_list.departnem = hoteldpt.depart

                        if res_line:
                            billbalance_list.ankunft = res_line.ankunft
                            billbalance_list.abreise = res_line.abreise
                            billbalance_list.resstatus = res_line.resstatus
                            billbalance_list.remarks = guest.bemerk + res_line.bemerk + bill.vesrdepot

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.CODE))).first()

                            if queasy:
                                billbalance_list.bill_inst = queasy.char1
                        else:

                            history = db_session.query(History).filter(
                                    (History.resnr == bill.resnr) &  (History.reslinnr < 999) &  (History.zi_wechsel == False)).first()

                            if history:
                                billbalance_list.ankunft = history.ankunft
                                billbalance_list.abreise = history.abreise


                        tot_outstand = tot_outstand + bill.saldo


        if co_today:

            if menu_fobill:

                bill_obj_list = []
                for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.reslinnr == Bill.reslinnr) &  (Res_line.abreise == ci_date)).filter(
                        (Bill.flag == 0) &  (Bill.resnr > 0) &  (func.lower(Bill.zinr) != "") &  (func.lower(Bill.zinr) >= (room).lower())).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    do_it = False

                    if zero_flag or bill.saldo != 0:
                        do_it = True

                    if gname != "":

                        reservation = db_session.query(Reservation).filter(
                                (func.lower(Reservation.groupname) == (gname).lower()) &  (Reservation.resnr == bill.resnr)).first()

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
                        billbalance_list.receiver = bill.name
                        billbalance_list.zipreis = res_line.zipreis
                        billbalance_list.rechnr = bill.rechnr
                        billbalance_list.saldo = bill.saldo
                        billbalance_list.ankunft = res_line.ankunft
                        billbalance_list.abreise = res_line.abreise
                        billbalance_list.idcard = guest.ausweis_nr1
                        billbalance_list.nat = guest.nation1
                        billbalance_list.datum = bill.datum
                        billbalance_list.fsort = "0"
                        billbalance_list.remarks = guest.bemerk + res_line.bemerk + bill.vesrdepot
                        billbalance_list.bill_remark = bill.vesrdepot

                        bill_line = db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == bill.rechnr)).first()

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                (Hoteldpt.num == 0)).first()

                        if hoteldpt:
                            billbalance_list.departnem = hoteldpt.depart

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.CODE))).first()

                        if queasy:
                            billbalance_list.bill_inst = queasy.char1
                        tot_outstand = tot_outstand + bill.saldo


        elif menu_fobill:

            for bill in db_session.query(Bill).filter(
                    (Bill.flag == 0) &  (Bill.resnr > 0) &  (func.lower(Bill.zinr) != "") &  (func.lower(Bill.zinr) >= (room).lower())).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

                if not res_line:

                    history = db_session.query(History).filter(
                            (History.resnr == bill.resnr) &  (History.reslinnr == bill.reslinnr) &  (not History.zi_wechsel)).first()
                do_it = False

                if zero_flag or bill.saldo != 0:
                    do_it = True

                if gname != "":

                    reservation = db_session.query(Reservation).filter(
                            (func.lower(Reservation.groupname) == (gname).lower()) &  (Reservation.resnr == bill.resnr)).first()

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
                    billbalance_list.zinr = bill.zinr
                    billbalance_list.receiver = bill.name
                    billbalance_list.rechnr = bill.rechnr
                    billbalance_list.saldo = bill.saldo
                    billbalance_list.idcard = guest.ausweis_nr1
                    billbalance_list.nat = guest.nation1
                    billbalance_list.datum = bill.datum
                    billbalance_list.fsort = "0"
                    billbalance_list.bill_remark = bill.vesrdepot

                    bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == bill.rechnr)).first()

                    hoteldpt = db_session.query(Hoteldpt).filter(
                            (Hoteldpt.num == 0)).first()

                    if hoteldpt:
                        billbalance_list.departnem = hoteldpt.depart

                    if res_line:
                        billbalance_list.ankunft = res_line.ankunft
                        billbalance_list.abreise = res_line.abreise
                        billbalance_list.zipreis = res_line.zipreis
                        billbalance_list.resstatus = res_line.resstatus
                        billbalance_list.remarks = guest.bemerk + res_line.bemerk + bill.vesrdepot

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.CODE))).first()

                        if queasy:
                            billbalance_list.bill_inst = queasy.char1

                    elif history:
                        billbalance_list.ankunft = history.ankunft
                        billbalance_list.abreise = history.abreise
                        billbalance_list.zipreis = history.zipreis


                    tot_outstand = tot_outstand + bill.saldo

    else:

        if co_today:

            if menu_fobill:

                bill_obj_list = []
                for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.reslinnr == Bill.reslinnr) &  (Res_line.abreise == ci_date)).filter(
                        (Bill.flag == 0) &  (Bill.resnr > 0) &  (func.lower(Bill.zinr) != "") &  (func.lower(Bill.zinr) >= (room).lower())).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:
                        do_it = False

                        if zero_flag or bill.saldo != 0:
                            do_it = True

                        if gname != "":

                            reservation = db_session.query(Reservation).filter(
                                    (func.lower(Reservation.groupname) == (gname).lower()) &  (Reservation.resnr == bill.resnr)).first()

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
                            billbalance_list.receiver = bill.name
                            billbalance_list.zipreis = res_line.zipreis
                            billbalance_list.rechnr = bill.rechnr
                            billbalance_list.saldo = bill.saldo
                            billbalance_list.ankunft = res_line.ankunft
                            billbalance_list.abreise = res_line.abreise
                            billbalance_list.idcard = guest.ausweis_nr1
                            billbalance_list.nat = guest.nation1
                            billbalance_list.datum = bill.datum
                            billbalance_list.fsort = "0"
                            billbalance_list.remarks = guest.bemerk + res_line.bemerk + bill.vesrdepot
                            billbalance_list.bill_remark = bill.vesrdepot

                            bill_line = db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == bill.rechnr)).first()

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                    (Hoteldpt.num == 0)).first()

                            if hoteldpt:
                                billbalance_list.departnem = hoteldpt.depart

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.CODE))).first()

                            if queasy:
                                billbalance_list.bill_inst = queasy.char1
                            tot_outstand = tot_outstand + bill.saldo

        else:

            if menu_fobill:

                for bill in db_session.query(Bill).filter(
                        (Bill.flag == 0) &  (Bill.resnr > 0) &  (func.lower(Bill.zinr) != "") &  (func.lower(Bill.zinr) >= (room).lower())).all():
                    do_it = False

                    if zero_flag or bill.saldo != 0:
                        do_it = True

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:

                        if do_it:

                            guest = db_session.query(Guest).filter(
                                    (Guest.gastnr == bill.gastnr)).first()
                            billbalance_list = Billbalance_list()
                            billbalance_list_list.append(billbalance_list)

                            billbalance_list.resstatus = res_line.resstatus
                            billbalance_list.zinr = bill.zinr
                            billbalance_list.receiver = bill.name
                            billbalance_list.rechnr = bill.rechnr
                            billbalance_list.saldo = bill.saldo
                            billbalance_list.idcard = guest.ausweis_nr1
                            billbalance_list.nat = guest.nation1
                            billbalance_list.datum = bill.datum
                            billbalance_list.fsort = "0"
                            billbalance_list.ankunft = res_line.ankunft
                            billbalance_list.abreise = res_line.abreise
                            billbalance_list.zipreis = res_line.zipreis
                            billbalance_list.bill_inst = queasy.char1
                            billbalance_list.remarks = guest.bemerk + res_line.bemerk + bill.vesrdepot
                            billbalance_list.bill_remark = bill.vesrdepot

                            bill_line = db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == bill.rechnr)).first()

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                    (Hoteldpt.num == 0)).first()

                            if hoteldpt:
                                billbalance_list.departnem = hoteldpt.depart

    billbalance_list = Billbalance_list()
    billbalance_list_list.append(billbalance_list)

    billbalance_list.receiver = "T o t a l"
    billbalance_list.saldo = tot_outstand
    billbalance_list.fsort = "1"

    return generate_output()