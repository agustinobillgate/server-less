#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 25/8/2025
# list kosong
# from functions import log_program_rd
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Htparam, Bill, Bill_line, Hoteldpt, Queasy, Res_line, History, Reservation

def bill_balance2_webbl(pvilanguage:int, co_today:bool, room:string, zero_flag:bool, cash_basis:bool, gname:string, billdate:date, menu_nsbill:bool, menu_msbill:bool, menu_fobill:bool):

    prepare_cache ([Guest, Htparam, Bill, Bill_line, Hoteldpt, Queasy, Res_line, History])

    billbalance_list_data = []
    tot_outstand:Decimal = to_decimal("0.0")
    bill_saldo:Decimal = to_decimal("0.0")
    tot_saldo:Decimal = to_decimal("0.0")
    do_it:bool = False
    ci_date:date = None
    lvcarea:string = "bill-balance"
    guest = htparam = bill = bill_line = hoteldpt = queasy = res_line = history = reservation = None

    billbalance_list = gast = None

    billbalance_list_data, Billbalance_list = create_model("Billbalance_list", {"flag":string, "departnem":string, "zinr":string, "resstatus":int, "zipreis":Decimal, "rechnr":int, "receiver":string, "ankunft":date, "abreise":date, "saldo":Decimal, "name":string, "bill_inst":string, "idcard":string, "nat":string, "datum":date, "fsort":string, "remarks":string, "bill_remark":string, "due_date":date}, {"ankunft": None, "abreise": None})

    Gast = create_buffer("Gast",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billbalance_list_data, tot_outstand, bill_saldo, tot_saldo, do_it, ci_date, lvcarea, guest, htparam, bill, bill_line, hoteldpt, queasy, res_line, history, reservation
        nonlocal pvilanguage, co_today, room, zero_flag, cash_basis, gname, billdate, menu_nsbill, menu_msbill, menu_fobill
        nonlocal gast

        nonlocal billbalance_list, gast
        nonlocal billbalance_list_data

        return {"billbalance-list": billbalance_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    
    # Rd 225/8/22025
    room = room.strip()
    gname = gname.strip()

    if not cash_basis:

        if not co_today:

            if room == "" and  menu_nsbill:
                for bill in db_session.query(Bill).filter(
                            (Bill.flag == 0) & (Bill.resnr == 0)
                            ).order_by(Bill.name).all():
                    do_it = False
                    bill_saldo =  to_decimal("0")

                    if (zero_flag and bill.datum != None and bill.name != "") or bill.saldo != 0:
                        do_it = True

                    if do_it:
                        billbalance_list = Billbalance_list()
                        billbalance_list_data.append(billbalance_list)

                        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                        # guest = db_session.query(Guest).filter(
                        #     (Guest.gastnr == bill.gastnr)
                        # ).first()
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

                            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, bill.billtyp)]})

                            if hoteldpt:
                                billbalance_list.departnem = hoteldpt.depart
                            billbalance_list.remarks = guest.bemerkung

                            queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})

                            if queasy:
                                billbalance_list.bill_inst = queasy.char1
                                billbalance_list.due_date = queasy.date1
                        tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)

            if room == "" and menu_msbill:
                for bill in db_session.query(Bill).filter(
                         (Bill.flag == 0) & (Bill.resnr > 0) & 
                         (Bill.reslinnr == 0)).order_by(Bill.name).all():
                    do_it = False
                    bill_saldo =  to_decimal("0")

                    if zero_flag or bill.saldo != 0:
                        do_it = True
                    do_it = True
                    if do_it:
                        billbalance_list = Billbalance_list()
                        billbalance_list_data.append(billbalance_list)

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(le, 8)]})
                        # res_line = (
                        #     db_session.query(Res_line)
                        #     .filter(
                        #         Res_line.resnr == bill.resnr,
                        #         Res_line.resstatus <= 8
                        #     )
                        #     .first()
                        # )

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

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

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

                        if hoteldpt:
                            billbalance_list.departnem = hoteldpt.depart

                        if res_line:
                            billbalance_list.ankunft = res_line.ankunft
                            billbalance_list.abreise = res_line.abreise
                            billbalance_list.resstatus = res_line.resstatus
                            billbalance_list.remarks = guest.bemerkung + res_line.bemerk + bill.vesrdepot

                            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                            if queasy:
                                billbalance_list.bill_inst = queasy.char1
                        else:

                            history = get_cache (History, {"resnr": [(eq, bill.resnr)],"reslinnr": [(lt, 999)],"zi_wechsel": [(eq, False)]})

                            if history:
                                billbalance_list.ankunft = history.ankunft
                                billbalance_list.abreise = history.abreise

                        queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})

                        if queasy:
                            billbalance_list.due_date = queasy.date1
                        tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)

        if co_today:

            if menu_fobill:
                bill_obj_list = {}
                bill = Bill()
                res_line = Res_line()
                for bill.name, bill.saldo, bill.gastnr, bill.rechnr, bill.datum, bill.vesrdepot, bill.billtyp, bill.resnr, bill.zinr, bill.reslinnr, \
                    bill.parent_nr, bill._recid, res_line.gastnrmember, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.bemerk, \
                    res_line.code, res_line.name, res_line.zipreis, res_line._recid \
                        in db_session.query(Bill.name, Bill.saldo, Bill.gastnr, Bill.rechnr, \
                                            Bill.datum, Bill.vesrdepot, Bill.billtyp, Bill.resnr, Bill.zinr, Bill.reslinnr, Bill.parent_nr, \
                                            Bill._recid, Res_line.gastnrmember, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, \
                                            Res_line.bemerk, Res_line.code, Res_line.name, Res_line.zipreis, Res_line._recid) \
                                    .join(Res_line,(Res_line.resnr == Bill.resnr) & 
                                          (Res_line.reslinnr == Bill.reslinnr) & 
                                          (Res_line.abreise == ci_date)) \
                                    .filter(
                                            (Bill.flag == 0) & 
                                            (Bill.resnr > 0) & 
                                            (Bill.zinr != "") & 
                                            (Bill.zinr >= room)) \
                                    .order_by(Bill.zinr, Bill.reslinnr).all():
                    
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    do_it = False
                    bill_saldo =  to_decimal("0")

                    if zero_flag or bill.saldo != 0:
                        do_it = True

                    if gname != "":

                        reservation = get_cache (Reservation, {"groupname": [(eq, gname)],"resnr": [(eq, bill.resnr)]})

                        if not reservation:
                            do_it = False

                    if do_it:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                        billbalance_list = Billbalance_list()
                        billbalance_list_data.append(billbalance_list)

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

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

                        if hoteldpt:
                            billbalance_list.departnem = hoteldpt.depart

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                        if queasy:
                            billbalance_list.bill_inst = queasy.char1

                        queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})

                        if queasy:
                            billbalance_list.due_date = queasy.date1
                        tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)

        elif menu_fobill:
            for bill in db_session.query(Bill).filter(
                     (Bill.flag == 0) & 
                     (Bill.resnr > 0) & (Bill.zinr != "") & 
                     (Bill.zinr >= room)).order_by(Bill.zinr, Bill.reslinnr).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
                if not res_line:
                    history = db_session.query(History).filter(
                             (History.resnr == bill.resnr) & (History.reslinnr == bill.reslinnr) & not_ (History.zi_wechsel)).first()
                
                do_it = False
                bill_saldo =  to_decimal("0")

                # if zero_flag or bill.saldo != 0:
                if zero_flag or bill.saldo != 0:
                    do_it = True
                
                if gname != "":

                    # reservation = get_cache (Reservation, {"groupname": [(eq, gname)],"resnr": [(eq, bill.resnr)]})
                    reservation = db_session(Reservation).filter(
                        (Reservation.groupname == gname) &
                        (Reservation.resnr == bill.resnr)
                    ).first()

                    if not reservation:
                        do_it = False

                if do_it:

                    if res_line:

                        # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember) 
                            ).first()
                    else:

                        # guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == bill.gastnr)
                            ).first()
                    billbalance_list = Billbalance_list()
                    billbalance_list_data.append(billbalance_list)


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

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

                    if hoteldpt:
                        billbalance_list.departnem = hoteldpt.depart

                    if res_line:
                        billbalance_list.ankunft = res_line.ankunft
                        billbalance_list.abreise = res_line.abreise
                        billbalance_list.zipreis =  to_decimal(res_line.zipreis)
                        billbalance_list.resstatus = res_line.resstatus
                        billbalance_list.remarks = res_line.bemerk + bill.vesrdepot

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                        if queasy:
                            billbalance_list.bill_inst = queasy.char1

                    elif history:
                        billbalance_list.ankunft = history.ankunft
                        billbalance_list.abreise = history.abreise
                        billbalance_list.zipreis =  to_decimal(history.zipreis)

                    queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})

                    if queasy:
                        billbalance_list.due_date = queasy.date1
                    tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)
    else:

        if co_today:

            if menu_fobill:
                bill_obj_list = {}
                bill = Bill()
                res_line = Res_line()
                for bill.name, bill.saldo, bill.gastnr, bill.rechnr, bill.datum, bill.vesrdepot, bill.billtyp, bill.resnr, bill.zinr, bill.reslinnr, bill.parent_nr, bill._recid, res_line.gastnrmember, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.bemerk, res_line.code, res_line.name, res_line.zipreis, res_line._recid in db_session.query(Bill.name, Bill.saldo, Bill.gastnr, Bill.rechnr, Bill.datum, Bill.vesrdepot, Bill.billtyp, Bill.resnr, Bill.zinr, Bill.reslinnr, Bill.parent_nr, Bill._recid, Res_line.gastnrmember, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.bemerk, Res_line.code, Res_line.name, Res_line.zipreis, Res_line._recid).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr) & (Res_line.abreise == ci_date)).filter(
                         (Bill.flag == 0) & (Bill.resnr > 0) & 
                         (Bill.zinr != "") & (Bill.zinr >= room)).order_by(Bill.zinr, Bill.reslinnr).all():
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True

                    queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})
                    if queasy and queasy.logi1:
                        do_it = False
                        bill_saldo =  to_decimal("0")

                        if zero_flag or bill.saldo != 0:
                            do_it = True

                        if gname != "":

                            reservation = get_cache (Reservation, {"groupname": [(eq, gname)],"resnr": [(eq, bill.resnr)]})

                            if not reservation:
                                do_it = False

                        if do_it:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                            billbalance_list = Billbalance_list()
                            billbalance_list_data.append(billbalance_list)

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

                            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

                            if hoteldpt:
                                billbalance_list.departnem = hoteldpt.depart

                            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                            if queasy:
                                billbalance_list.bill_inst = queasy.char1

                            queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})

                            if queasy:
                                billbalance_list.due_date = queasy.date1
                            tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)
        else:

            if menu_fobill:

                for bill in db_session.query(Bill).filter(
                         (Bill.flag == 0) & (Bill.resnr > 0) & 
                         (Bill.zinr != "") & 
                         (Bill.zinr >= room)).order_by(Bill.zinr, Bill.reslinnr).all():
                    do_it = False
                    bill_saldo =  to_decimal("0")
                    if zero_flag or bill.saldo != 0:
                        do_it = True
                    
                    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})
                    # res_line = (
                    #             db_session.query(Res_line)
                    #             .filter(
                    #                 Res_line.resnr == bill.resnr,
                    #                 Res_line.reslinnr == bill.parent_nr
                    #             )
                    #             .first()
                    #         )
                    queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})
                    # queasy = db_session.query(Queasy).filter(
                    #     (Queasy.key==9) &
                    #     (Queasy.number1 == to_int(Res_line.code))
                    #     ).first()

                    if queasy and queasy.logi1:

                        if do_it:

                            # guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                            guest = db_session.query(Guest).filter(
                                (Guest.gastnr == bill.gastnr)
                            ).first()

                            for bill_line in db_session.query(Bill_line).filter(
                                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line._recid).all():
                                bill_saldo =  to_decimal(bill_saldo) + to_decimal(bill_line.betrag)
                            tot_saldo =  to_decimal(tot_saldo) + to_decimal(bill_saldo)
                            billbalance_list = Billbalance_list()
                            billbalance_list_data.append(billbalance_list)

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

                            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

                            if hoteldpt:
                                billbalance_list.departnem = hoteldpt.depart

                            queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})

                            if queasy:
                                billbalance_list.due_date = queasy.date1
                            tot_outstand =  to_decimal(tot_outstand) + to_decimal(tot_saldo)
    tot_outstand =  to_decimal("0")

    for billbalance_list in query(billbalance_list_data):
        tot_outstand =  to_decimal(tot_outstand) + to_decimal(billbalance_list.saldo)
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr_unicode(10) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr_unicode(13) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "~n", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "\\n", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "~r", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "~r~n", "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "&nbsp;", " ")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "</p>", chr_unicode(13))
        billbalance_list.remarks = replace_str(billbalance_list.remarks, "<BR>", chr_unicode(13))
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr_unicode(10) + chr_unicode(13) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr_unicode(2) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr_unicode(3) , "")
        billbalance_list.remarks = replace_str(billbalance_list.remarks, chr_unicode(4) , "")

        if length(billbalance_list.remarks) < 3:
            billbalance_list.remarks = replace_str(billbalance_list.remarks, chr_unicode(32) , "")

        if length(billbalance_list.remarks) < 3:
            billbalance_list.remarks = ""

        if length(billbalance_list.remarks) == None:
            billbalance_list.remarks = ""
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr_unicode(10) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr_unicode(13) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "~n", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "\\n", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "~r", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "~r~n", "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "&nbsp;", " ")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "</p>", chr_unicode(13))
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, "<BR>", chr_unicode(13))
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr_unicode(10) + chr_unicode(13) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr_unicode(2) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr_unicode(3) , "")
        billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr_unicode(4) , "")

        if length(billbalance_list.bill_remark) < 3:
            billbalance_list.bill_remark = replace_str(billbalance_list.bill_remark, chr_unicode(32) , "")

        if length(billbalance_list.bill_remark) < 3:
            billbalance_list.bill_remark = ""

        if length(billbalance_list.bill_remark) == None:
            billbalance_list.bill_remark = ""
    billbalance_list = Billbalance_list()
    billbalance_list_data.append(billbalance_list)

    billbalance_list.receiver = "T o t a l"
    billbalance_list.saldo =  to_decimal(tot_outstand)
    billbalance_list.fsort = "1"

    return generate_output()