#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Res_line, Waehrung, Guest

def mast_member_webbl(resno:int, billno:int):

    prepare_cache ([Bill, Res_line, Waehrung, Guest])

    tot_adult = 0
    tot_room = 0
    b1_list_list = []
    bill = res_line = waehrung = guest = None

    b_list = b1_list = mbill = None

    b_list_list, B_list = create_model("B_list", {"resnr":int, "reslinnr":int, "rechnr":int, "saldo":Decimal, "parent_nr":int})
    b1_list_list, B1_list = create_model("B1_list", {"resnr":int, "reslinnr":int, "zinr":string, "name":string, "erwachs":int, "rechnr":int, "saldo":Decimal, "resstatus":int, "ankunft":date, "abreise":date, "gname":string, "gratis":int, "kind1":int, "kind2":int, "arrangement":string, "zipreis":Decimal, "wabkurz":string, "bill_name":string})

    Mbill = create_buffer("Mbill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_adult, tot_room, b1_list_list, bill, res_line, waehrung, guest
        nonlocal resno, billno
        nonlocal mbill


        nonlocal b_list, b1_list, mbill
        nonlocal b_list_list, b1_list_list

        return {"billno": billno, "tot_adult": tot_adult, "tot_room": tot_room, "b1-list": b1_list_list}


    bill = get_cache (Bill, {"rechnr": [(eq, billno)]})

    if bill.reslinnr == 0:

        mbill = get_cache (Bill, {"rechnr": [(eq, billno)]})
    else:

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

        if res_line.l_zuordnung[4] != 0:

            mbill = get_cache (Bill, {"resnr": [(eq, res_line.l_zuordnung[4])],"reslinnr": [(eq, 0)]})
        else:

            mbill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})

        if not mbill:

            return generate_output()
    billno = mbill.rechnr

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resno) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

        if res_line.resstatus != 12 and res_line.resstatus != 99:
            tot_adult = tot_adult + res_line.erwachs

        if res_line.resstatus != 12 and res_line.resstatus != 13 and res_line.resstatus != 99 and not res_line.zimmerfix:
            tot_room = tot_room + res_line.zimmeranz

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
        b_list = B_list()
        b_list_list.append(b_list)

        b_list.resnr = res_line.resnr
        b_list.reslinnr = res_line.reslinnr

        if bill:
            b_list.rechnr = bill.rechnr
            b_list.saldo =  to_decimal(bill.saldo)
            b_list.parent_nr = bill.parent_nr

    for res_line in db_session.query(Res_line).filter(
             (Res_line.l_zuordnung[inc_value(4)] == resno) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.resnr != resno)).order_by(Res_line._recid).all():

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
        b_list = B_list()
        b_list_list.append(b_list)

        b_list.resnr = res_line.resnr
        b_list.reslinnr = res_line.reslinnr

        if bill:
            b_list.rechnr = bill.rechnr
            b_list.saldo =  to_decimal(bill.saldo)
            b_list.parent_nr = bill.parent_nr

    res_line_obj_list = {}
    for res_line in db_session.query(Res_line).filter(
             ((Res_line.resnr == resno) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.l_zuordnung[inc_value(2)] == 0)) | ((Res_line.l_zuordnung[inc_value(4)] == resno) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.active_flag <= 1) & (Res_line.resnr != resno))).order_by(Res_line.zinr, b_list.parent_nr, Res_line.name).all():
        b_list = query(b_list_list, (lambda b_list: b_list.resnr == res_line.resnr and b_list.reslinnr == res_line.reslinnr), first=True)
        if not b_list:
            continue

        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.zinr = res_line.zinr
        b1_list.erwachs = res_line.erwachs
        b1_list.rechnr = b_list.rechnr
        b1_list.saldo =  to_decimal(b_list.saldo)
        b1_list.resstatus = res_line.resstatus
        b1_list.ankunft = res_line.ankunft
        b1_list.abreise = res_line.abreise
        b1_list.resnr = res_line.resnr
        b1_list.reslinnr = res_line.reslinnr
        b1_list.erwachs = res_line.erwachs
        b1_list.gratis = res_line.gratis
        b1_list.kind1 = res_line.kind1
        b1_list.kind2 = res_line.kind2
        b1_list.arrangement = res_line.arrangement
        b1_list.zipreis =  to_decimal(res_line.zipreis)

        if res_line.resstatus != 12:
            b1_list.gname = res_line.name

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if waehrung:
            b1_list.wabkurz = waehrung.wabkurz
        else:
            b1_list.wabkurz = " "

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        if guest:
            b1_list.bill_name = guest.name + ", " + guest.vorname1 +\
                    guest.anredefirma + " " + guest.anrede1

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            b1_list.name = guest.name + ", " + guest.vorname1 +\
                    guest.anredefirma + " " + guest.anrede1

    return generate_output()