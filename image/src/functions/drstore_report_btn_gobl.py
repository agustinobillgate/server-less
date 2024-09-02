from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import H_journal, Kellner, H_bill, Bill, Res_line, H_artikel, Artikel, Wgrpdep

def drstore_report_btn_gobl(usr_created:bool, dstore_dept:int, all_flag:bool, ekumnr:int, zknr1:int, zknr2:int, zknr3:int, zknr4:int, zknr5:int, zknr6:int, from_date:date, to_date:date, usr_init:str):
    exchg_rate = 0
    t_betrag = 0
    t_foreign = 0
    s_list_list = []
    pay_list_list = []
    h_journal = kellner = h_bill = bill = res_line = h_artikel = artikel = wgrpdep = None

    s_list = pay_list = usr_list = sbuff = None

    s_list_list, S_list = create_model("S_list", {"zinr":str, "gname":str, "rechnr":int, "zknr":[int, 6], "anzahl":int, "amount":decimal, "tamount":decimal, "tanz":int, "userinit":str})
    pay_list_list, Pay_list = create_model("Pay_list", {"flag":int, "bezeich":str, "artnr":int, "rechnr":int, "foreign":decimal, "saldo":decimal})
    usr_list_list, Usr_list = create_model("Usr_list", {"kellner_nr":int, "kellnername":str})

    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, t_betrag, t_foreign, s_list_list, pay_list_list, h_journal, kellner, h_bill, bill, res_line, h_artikel, artikel, wgrpdep
        nonlocal sbuff


        nonlocal s_list, pay_list, usr_list, sbuff
        nonlocal s_list_list, pay_list_list, usr_list_list
        return {"exchg_rate": exchg_rate, "t_betrag": t_betrag, "t_foreign": t_foreign, "s-list": s_list_list, "pay-list": pay_list_list}

    def create_list_all():

        nonlocal exchg_rate, t_betrag, t_foreign, s_list_list, pay_list_list, h_journal, kellner, h_bill, bill, res_line, h_artikel, artikel, wgrpdep
        nonlocal sbuff


        nonlocal s_list, pay_list, usr_list, sbuff
        nonlocal s_list_list, pay_list_list, usr_list_list

        for h_journal in db_session.query(H_journal).filter(
                    (H_journal.departement == dstore_dept) &  (H_journal.bill_datum == from_date)).all():

            kellner = db_session.query(Kellner).filter(
                        (Kellner_nr == h_journal.kellner_nr) &  (Kellner.departement == dstore_dept)).first()

            if kellner:

                usr_list = query(usr_list_list, filters=(lambda usr_list :usr_list.kellner_nr == h_journal.kellner_nr), first=True)

                if not usr_list:
                    usr_list = Usr_list()
                    usr_list_list.append(usr_list)

                    usr_list.kellner_nr = h_journal.kellner_nr
                    usr_list.kellnername = kellnername


        usr_created = True

        for usr_list in query(usr_list_list):
            create_list(to_string(usr_list.kellner_nr), usr_list.kellnername)

        if all_flag:
            sbuff = Sbuff()
            sbuff_list.append(sbuff)

            sbuff.gname = "Grand Total"

            for s_list in query(s_list_list, filters=(lambda s_list :not re.match(".*Total.*",s_list.gname))):
                sbuff.anzahl[0] = sbuff.anzahl[0] + s_list.anzahl[0]
                sbuff.anzahl[1] = sbuff.anzahl[1] + s_list.anzahl[1]
                sbuff.anzahl[2] = sbuff.anzahl[2] + s_list.anzahl[2]
                sbuff.anzahl[3] = sbuff.anzahl[3] + s_list.anzahl[3]
                sbuff.anzahl[4] = sbuff.anzahl[4] + s_list.anzahl[4]
                sbuff.anzahl[5] = sbuff.anzahl[5] + s_list.anzahl[5]
                sbuff.amount[0] = sbuff.amount[0] + s_list.amount[0]
                sbuff.amount[1] = sbuff.amount[1] + s_list.amount[1]
                sbuff.amount[2] = sbuff.amount[2] + s_list.amount[2]
                sbuff.amount[3] = sbuff.amount[3] + s_list.amount[3]
                sbuff.amount[4] = sbuff.amount[4] + s_list.amount[4]
                sbuff.amount[5] = sbuff.amount[5] + s_list.amount[5]
                sbuff.tanz = sbuff.tanz + s_list.tanz
                sbuff.tamount = sbuff.tamount + s_list.tamount

    def create_list(usr_init:str, kellner_name:str):

        nonlocal exchg_rate, t_betrag, t_foreign, s_list_list, pay_list_list, h_journal, kellner, h_bill, bill, res_line, h_artikel, artikel, wgrpdep
        nonlocal sbuff


        nonlocal s_list, pay_list, usr_list, sbuff
        nonlocal s_list_list, pay_list_list, usr_list_list

        curr_date:date = None
        rmno:str = ""
        billno:int = 0
        gname:str = ""
        t_qty:[int] = [0, 0, 0, 0, 0, 0, 0]
        t_amt:[decimal] = [0, 0, 0, 0, 0, 0, 0]
        tot_qty:int = 0
        tot_amt:decimal = 0
        disc_art:bool = False
        qty_i:int = 0
        for curr_date in range(from_date,to_date + 1) :

            h_journal_obj_list = []
            for h_journal, h_bill in db_session.query(H_journal, H_bill).join(H_bill,(H_bill.rechnr == H_journal.rechnr) &  (H_bill.departement == H_journal.departement)).filter(
                    (H_journal.kellner_nr == to_int(usr_init)) &  (H_journal.departement == dstore_dept) &  (H_journal.bill_datum == curr_date)).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)

                if h_journal.artnr == 0 and substring(h_journal.bezeich, 6, 4) == "rmno":

                    pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 2), first=True)

                    if not pay_list:
                        pay_list = Pay_list()
                        pay_list_list.append(pay_list)

                        pay_list.flag = 2
                        pay_list.bezeich = "Room Transfer"
                    pay_list.foreign = pay_list.foreign - h_journal.fremdwaehrng
                    pay_list.saldo = pay_list.saldo - h_journal.betrag
                    t_betrag = t_betrag - h_journal.betrag
                    t_foreign = t_foreign - h_journal.fremdwaehrng
                    rmno = substring(h_journal.bezeich, 11, 6)

                    if substring(rmno, 5, 1) == "*":
                        rmno = substring(rmno, 0, 5)
                        billno = to_int(substring(h_journal.bezeich, 16, 10))
                    else:
                        billno = to_int(substring(h_journal.bezeich, 17, 10))

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == billno)).first()

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

                    if res_line:
                        gname = res_line.name

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.rechnr == h_journal.rechnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.rechnr = h_journal.rechnr
                    s_list.zinr = rmno
                    s_list.gname = gname

                elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 8) == "Transfer":
                    gname = "BillTransfer"
                    billno = to_int(substring(h_journal.bezeich, 10, 10))

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == billno)).first()

                    if bill:
                        gname = bill.name

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.rechnr == h_journal.rechnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.rechnr = h_journal.rechnr
                    s_list.gname = gname

                    pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 3), first=True)

                    if not pay_list:
                        pay_list = Pay_list()
                        pay_list_list.append(pay_list)

                        pay_list.flag = 3
                        pay_list.bezeich = "Bill Transfer"
                    pay_list.foreign = pay_list.foreign - h_journal.fremdwaehrng
                    pay_list.saldo = pay_list.saldo - h_journal.betrag
                    t_betrag = t_betrag - h_journal.betrag
                    t_foreign = t_foreign - h_journal.fremdwaehrng

                elif h_journal.artnr > 0:

                    h_artikel = db_session.query(H_artikel).filter(
                            (H_artikel.artnr == h_journal.artnr) &  (H_artikel.departement == h_journal.departement)).first()

                    if h_artikel.artart == 2 or h_artikel.artart == 7 or h_artikel.artart == 6 or h_artikel.artart == 11:

                        if h_artikel.artart == 6:

                            pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 1), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 1
                                pay_list.bezeich = "Cash"

                        elif h_artikel.artart == 7:

                            pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 4), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 4
                                pay_list.bezeich = "Credit Card"

                        elif h_artikel.artart == 2:

                            pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 5), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 5
                                pay_list.bezeich = "City Ledger"

                        elif h_artikel.artart == 11:

                            pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 6), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 6
                                pay_list.bezeich = "Compliment"


                        pay_list.foreign = pay_list.foreign - h_journal.fremdwaehrng
                        pay_list.saldo = pay_list.saldo - h_journal.betrag
                        t_betrag = t_betrag - h_journal.betrag
                        t_foreign = t_foreign - h_journal.fremdwaehrng

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.rechnr == h_journal.rechnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.rechnr = h_journal.rechnr
                        s_list.gname = h_artikel.bezeich

                    elif h_artikel.artart == 0:
                        disc_art = False
                        qty_i = h_journal.anzahl

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                        if artikel.endkum == ekumnr:
                            disc_art = True
                            qty_i = 0

                        wgrpdep = db_session.query(Wgrpdep).filter(
                                (Wgrpdep.zknr == h_artikel.zwkum) &  (Wgrpdep.departement == h_artikel.departement)).first()

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.rechnr == h_journal.rechnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.rechnr = h_journal.rechnr

                        if wgrpdep.zknr == zknr1:
                            s_list.zknr[0] = wgrpdep.zknr
                            s_list.anzahl[0] = s_list.anzahl[0] + qty_i
                            s_list.amount[0] = s_list.amount[0] + h_journal.betrag
                            t_qty[0] = t_qty[0] + qty_i
                            t_amt[0] = t_amt[0] + h_journal.betrag

                        elif wgrpdep.zknr == zknr2:
                            s_list.zknr[1] = wgrpdep.zknr
                            s_list.anzahl[1] = s_list.anzahl[1] + qty_i
                            s_list.amount[1] = s_list.amount[1] + h_journal.betrag
                            t_qty[1] = t_qty[1] + qty_i
                            t_amt[1] = t_amt[1] + h_journal.betrag

                        elif wgrpdep.zknr == zknr3:
                            s_list.zknr[2] = wgrpdep.zknr
                            s_list.anzahl[2] = s_list.anzahl[2] + qty_i
                            s_list.amount[2] = s_list.amount[2] + h_journal.betrag
                            t_qty[2] = t_qty[2] + qty_i
                            t_amt[2] = t_amt[2] + h_journal.betrag

                        elif wgrpdep.zknr == zknr4:
                            s_list.zknr[3] = wgrpdep.zknr
                            s_list.anzahl[3] = s_list.anzahl[3] + qty_i
                            s_list.amount[3] = s_list.amount[3] + h_journal.betrag
                            t_qty[3] = t_qty[3] + qty_i
                            t_amt[3] = t_amt[3] + h_journal.betrag

                        elif wgrpdep.zknr == zknr5:
                            s_list.zknr[4] = wgrpdep.zknr
                            s_list.anzahl[4] = s_list.anzahl[4] + qty_i
                            s_list.amount[4] = s_list.amount[4] + h_journal.betrag
                            t_qty[4] = t_qty[4] + qty_i
                            t_amt[4] = t_amt[4] + h_journal.betrag

                        elif wgrpdep.zknr == zknr6:
                            s_list.zknr[5] = wgrpdep.zknr
                            s_list.anzahl[5] = s_list.anzahl[5] + qty_i
                            s_list.amount[5] = s_list.amount[5] + h_journal.betrag
                            t_qty[5] = t_qty[5] + qty_i
                            t_amt[5] = t_amt[5] + h_journal.betrag
                        tot_qty = tot_qty + qty_i
                        tot_amt = tot_amt + h_journal.betrag
                        s_list.tanz = s_list.tanz + qty_i
                        s_list.tamount = s_list.tamount + h_journal.betrag

                        if h_journal.fremdwaehrng != 0:
                            exchg_rate = h_journal.betrag / h_journal.fremdwaehrng
        s_list = S_list()
        s_list_list.append(s_list)


        if not all_flag:
            s_list.gname = "T o t a l"
        else:
            s_list.gname = "Total - " + kellner_name
        s_list.anzahl[0] = t_qty[0]
        s_list.anzahl[1] = t_qty[1]
        s_list.anzahl[2] = t_qty[2]
        s_list.anzahl[3] = t_qty[3]
        s_list.anzahl[4] = t_qty[4]
        s_list.anzahl[5] = t_qty[5]
        s_list.amount[0] = t_amt[0]
        s_list.amount[1] = t_amt[1]
        s_list.amount[2] = t_amt[2]
        s_list.amount[3] = t_amt[3]
        s_list.amount[4] = t_amt[4]
        s_list.amount[5] = t_amt[5]
        s_list.tanz = tot_qty
        s_list.tamount = tot_amt

    if all_flag:
        create_list_all()
    else:
        create_list(usr_init, "")

    return generate_output()