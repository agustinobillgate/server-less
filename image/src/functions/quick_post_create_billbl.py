from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Bill, Artikel, Counters, Htparam, Bill_line, Umsatz, Billjournal, Master, Mast_art

def quick_post_create_billbl(s_list:[S_list], pvilanguage:int, billart:int, curr_dept:int, amount:decimal, double_currency:bool, foreign_rate:bool, user_init:str, voucher_nr:str):
    msg_str = ""
    msg_str2 = ""
    lvcarea:str = "quick_post"
    res_line = bill = artikel = counters = htparam = bill_line = umsatz = billjournal = master = mast_art = None

    s_list = resline = None

    s_list_list, S_list = create_model("S_list", {"zeit":int, "dept":int, "artnr":int, "bezeich":str, "zinr":str, "anzahl":int, "preis":decimal, "betrag":decimal, "l_betrag":decimal, "f_betrag":decimal, "resnr":int, "reslinnr":int})

    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, lvcarea, res_line, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal resline


        nonlocal s_list, resline
        nonlocal s_list_list
        return {"msg_str": msg_str, "msg_str2": msg_str2}

    def create_bill():

        nonlocal msg_str, msg_str2, lvcarea, res_line, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal resline


        nonlocal s_list, resline
        nonlocal s_list_list

        for s_list in query(s_list_list):

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == s_list.resnr) &  (Res_line.reslinnr == s_list.reslinnr)).first()

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr) &  (Bill.zinr == res_line.zinr)).first()

            if bill.flag == 1:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("Bill Number", lvcarea, "") + " " + to_string(bill.rechnr) + " " + translateExtended ("RmNo", lvcarea, "") + " " + s_list.zinr + " : " + translateExtended ("Status closed, Posting not possible.", lvcarea, "")
            else:

                if res_line.l_zuordnung[1] != 1:
                    check_mbill()
                update_bill()
            s_list_list.remove(s_list)

    def update_bill():

        nonlocal msg_str, msg_str2, lvcarea, res_line, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal resline


        nonlocal s_list, resline
        nonlocal s_list_list

        bil_flag:int = 0
        master_flag:bool = False
        bill_date:date = None
        na_running:bool = False

        bill = db_session.query(Bill).first()

        artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == billart) &  (Artikel.departement == curr_dept)).first()

        if artikel.umsatzart == 1:
            bill.logisumsatz = bill.logisumsatz + amount

        elif artikel.umsatzart == 2:
            bill.argtumsatz = bill.argtumsatz + amount

        elif (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
            bill.f_b_umsatz = bill.f_b_umsatz + amount

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz = bill.sonst_umsatz + amount

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
            bill.gesamtumsatz = bill.gesamtumsatz + amount
        bill.rgdruck = 0
        bill.saldo = bill.saldo + s_list.l_betrag

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + s_list.f_betrag

        if bill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 3)).first()
            counters = counters + 1
            bill.rechnr = counters

            counters = db_session.query(Counters).first()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 253)).first()
        na_running = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        if na_running and bill_date == fdate:
            bill_date = bill_date + 1

        if bill.datum < bill_date or bill.datum == None:
            bill.datum = bill_date

        bill = db_session.query(Bill).first()
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = s_list.artnr
        bill_line.bezeich = s_list.bezeich
        bill_line.anzahl = s_list.anzahl
        bill_line.betrag = s_list.l_betrag
        bill_line.fremdwbetrag = s_list.f_betrag
        bill_line.zinr = s_list.zinr
        bill_line.departement = s_list.dept
        bill_line.epreis = s_list.preis
        bill_line.zeit = s_list.zeit
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date

        bill_line = db_session.query(Bill_line).first()

        umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == s_list.artnr) &  (Umsatz.departement == s_list.dept) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = s_list.artnr
            umsatz.datum = bill_date
            umsatz.departement = s_list.dept
        umsatz.betrag = umsatz.betrag + s_list.l_betrag
        umsatz.anzahl = umsatz.anzahl + s_list.anzahl

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = s_list.artnr
        billjournal.anzahl = s_list.anzahl
        billjournal.fremdwaehrng = s_list.f_betrag
        billjournal.betrag = s_list.l_betrag
        billjournal.bezeich = s_list.bezeich
        billjournal.zinr = s_list.zinr
        billjournal.departement = s_list.dept
        billjournal.epreis = s_list.preis
        billjournal.zeit = s_list.zeit
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

        if artikel.artart == 2 or artikel.artart == 7:
            inv_ar(artikel.artnr, res_line.zinr, bill.gastnr, res_line.gastnrmember, bill.rechnr, s_list.betrag, s_list.f_betrag, bill_date, bill.name, user_init, voucher_nr)

    def check_mbill():

        nonlocal msg_str, msg_str2, lvcarea, res_line, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal resline


        nonlocal s_list, resline
        nonlocal s_list_list

        master_flag:bool = False
        Resline = Res_line

        master = db_session.query(Master).filter(
                (Master.resnr == bill.resnr) &  (Master.active) &  (Master.flag == 0)).first()

        if master:

            if (master.umsatzart[0]  and artikel.artart == 8) or (master.umsatzart[1]  and artikel.artart == 9 and artikel.artgrp == 0) or (master.umsatzart[2]  and artikel.umsatzart == 3) or (master.umsatzart[3]  and artikel.umsatzart == 4):
                master_flag = True

            if not master_flag:

                mast_art = db_session.query(Mast_art).filter(
                        (Mast_art.resnr == master.resnr) &  (Mast_art.departement == artikel.departement) &  (Mast_art.artnr == artikel.artnr)).first()

                if mast_art:
                    master_flag = True

        if master_flag:

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == 0)).first()
            msg_str2 = translateExtended ("RmNo", lvcarea, "") + " " + res_line.zinr + " " + translateExtended ("transfered to Master Bill No.", lvcarea, "") + " " + to_string(bill.rechnr)

            return

        if res_line.memozinr != "" and res_line.memozinr != res_line.zinr:

            resline = db_session.query(Resline).filter(
                    (Resline.zinr == res_line.memozinr) &  (Resline.resstatus == 6)).first()

            if resline:

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == resline.resnr) &  (Bill.reslinnr == resline.reslinnr)).first()
            msg_str2 = translateExtended ("RmNo", lvcarea, "") + " " + res_line.zinr + " " + translateExtended ("transfered to Bill No.", lvcarea, "") + " " + to_string(bill.rechnr)


    create_bill()

    return generate_output()