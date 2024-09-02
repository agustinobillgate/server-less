from functions.additional_functions import *
import decimal
from models import Bill, Res_line, Waehrung

def mast_memberbl(resno:int, billno:int):
    tot_adult = 0
    tot_room = 0
    b1_list_list = []
    bill = res_line = waehrung = None

    b_list = b1_list = mbill = None

    b_list_list, B_list = create_model("B_list", {"resnr":int, "reslinnr":int, "rechnr":int, "saldo":decimal, "parent_nr":int})
    b1_list_list, B1_list = create_model("B1_list", {"resnr":int, "reslinnr":int, "zinr":str, "name":str, "erwachs":int, "rechnr":int, "saldo":decimal, "resstatus":int, "ankunft":date, "abreise":date, "gname":str, "gratis":int, "kind1":int, "kind2":int, "arrangement":str, "zipreis":decimal, "wabkurz":str})

    Mbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_adult, tot_room, b1_list_list, bill, res_line, waehrung
        nonlocal mbill


        nonlocal b_list, b1_list, mbill
        nonlocal b_list_list, b1_list_list
        return {"tot_adult": tot_adult, "tot_room": tot_room, "b1-list": b1_list_list}


    bill = db_session.query(Bill).filter(
            (Bill.rechnr == billno)).first()

    if bill.reslinnr == 0:

        mbill = db_session.query(Mbill).filter(
                (Mbill.rechnr == billno)).first()
    else:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

        if res_line.l_zuordnung[4] != 0:

            mbill = db_session.query(Mbill).filter(
                    (Mbill.resnr == res_line.l_zuordnung[4]) &  (Mbill.reslinnr == 0)).first()
        else:

            mbill = db_session.query(Mbill).filter(
                    (Mbill.resnr == res_line.resnr) &  (Mbill.reslinnr == 0)).first()

        if not mbill:

            return generate_output()
    billno = mbill.rechnr

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 99) &  (Res_line.l_zuordnung[2] == 0)).all():

        if res_line.resstatus != 12 and res_line.resstatus != 99:
            tot_adult = tot_adult + res_line.erwachs

        if res_line.resstatus != 12 and res_line.resstatus != 13 and res_line.resstatus != 99 and not res_line.zimmerfix:
            tot_room = tot_room + res_line.zimmeranz

        bill = db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()
        b_list = B_list()
        b_list_list.append(b_list)

        b_list.resnr = res_line.resnr
        b_list.reslinnr = res_line.reslinnr

        if bill:
            b_list.rechnr = bill.rechnr
            b_list.saldo = bill.saldo
            b_list.parent_nr = bill.parent_nr

    for res_line in db_session.query(Res_line).filter(
            (Res_line.l_zuordnung[4] == resno) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (Res_line.resnr != resno)).all():

        bill = db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()
        b_list = B_list()
        b_list_list.append(b_list)

        b_list.resnr = res_line.resnr
        b_list.reslinnr = res_line.reslinnr

        if bill:
            b_list.rechnr = bill.rechnr
            b_list.saldo = bill.saldo
            b_list.parent_nr = bill.parent_nr

    res_line_obj_list = []
    for res_line, b_list in db_session.query(Res_line, B_list).join(B_list,(B_list.resnr == Res_line.resnr) &  (B_list.reslinnr == Res_line.reslinnr)).filter(
            ((Res_line.resnr == resno) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.l_zuordnung[2] == 0)) |  ((Res_line.l_zuordnung[4] == resno) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99) &  (Res_line.active_flag <= 1) &  (Res_line.resnr != resno))).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.zinr = res_line.zinr
        b1_list.name = res_line.name
        b1_list.erwachs = res_line.erwachs
        b1_list.rechnr = b_list.rechnr
        b1_list.saldo = b_list.saldo
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
        b1_list.zipreis = res_line.zipreis

        if res_line.resstatus != 12:
            b1_list.gname = res_line.name

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == res_line.betriebsnr)).first()

        if waehrung:
            b1_list.wabkurz = waehrung.wabkurz
        else:
            b1_list.wabkurz = "    "

    return generate_output()